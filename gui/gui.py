__author__ = 'Celery'

import pygtk
pygtk.require('2.0')
import gtk
from midi.main import Engine


class Gui:
    def new_menu_item(self, name, img, accel, func):
        if name == 'sep':
            return gtk.SeparatorMenuItem()
        menu_item = gtk.ImageMenuItem(img, name)
        menu_item.connect('activate', func, name)
        key, mod = gtk.accelerator_parse(accel)
        menu_item.add_accelerator('activate', self.shortcuts, key, mod, gtk.ACCEL_VISIBLE)
        menu_item.show()
        return menu_item

    def create_menu(self):
        items = [['New',    gtk.STOCK_NEW,      '<Control>N',       self.new_file],
                 ['Open',   gtk.STOCK_OPEN,     '<Control>O',       self.open_file],
                 ['Save As',gtk.STOCK_SAVE_AS,  '<Control><Shift>S',self.new_file],
                 ['Save',   gtk.STOCK_SAVE,     '<Control>S',       self.save_file],
                 ['sep',    None,               None,               None],
                 ['Quit',   gtk.STOCK_QUIT,     '<Control>Q',       self.delete_event]]

        self.menu = gtk.Menu()
        self.shortcuts = gtk.AccelGroup()
        self.window.add_accel_group(self.shortcuts)

        for name, img, accel, func in items:
            menu_item = self.new_menu_item(name, img, accel, func)
            self.menu.append(menu_item)

        self.file_menu = gtk.MenuItem('File')
        self.file_menu.set_submenu(self.menu)
        self.file_menu.show()

        self.menu_separator = gtk.VBox()
        self.window.add(self.menu_separator)
        self.menu_separator.show()

        self.menu_bar = gtk.MenuBar()
        self.menu_separator.pack_start(self.menu_bar, False, False, 2)
        self.menu_bar.append(self.file_menu)
        self.menu_bar.show()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('TopHat MIDI')
        self.window.set_size_request(250, 200)

        self.window.connect("delete_event", self.delete_event)

        self.create_menu()

        self.window.show()

    def new_file(self, widget, event, data=None):
        if event == 'New':
            title = 'Create a new file'
        elif event == 'Save As':
            title = 'Save as'
        new_file_window = gtk.FileChooserDialog(title=title,
                                                parent=self.window,
                                                action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                                buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        filename_label = gtk.Label('Enter a filename:')
        filename_input = gtk.Entry()
        filename_bar = gtk.HBox(spacing=10)
        filename_bar.pack_start(filename_label, expand=False)
        filename_bar.pack_start(filename_input)
        filename_label.show()
        filename_input.show()
        new_file_window.set_extra_widget(filename_bar)
        event = new_file_window.run()

        if event == gtk.RESPONSE_OK:
            print filename_input.get_text(), new_file_window.get_filename()
            engine.new_file(filename_input.get_text(), new_file_window.get_filename())

        new_file_window.destroy()

    def open_file(self, widget, event, data=None):
        open_file_window = gtk.FileChooserDialog(title='Select a file to open',
                                                 parent=self.window,
                                                 buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        event = open_file_window.run()
        if event == gtk.RESPONSE_OK:
            engine.open(open_file_window.get_filename())

        open_file_window.destroy()

    def save_file(self, widget, event, data=None):
        engine.save()

    def save_as(self, widget, event, data=None):
        pass

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def button_press(self, widget, event):
        if event.type == gtk.gdk.BUTTON_PRESS:
            widget.popup(None, None, None, event.button, event.time)
            return True
        return False

    def menuitem_response(self, widget, string):
        print "%s" % string

if __name__ == "__main__":
    engine = Engine()
    gui = Gui()
    gtk.main()
