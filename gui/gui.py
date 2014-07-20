__author__ = 'Celery'

import pygtk
pygtk.require('2.0')
import gtk
from widgets.key_widg import KeyWidg
from widgets.pot_widg import PotWidg
from midi.main import Engine
import midi.defaults.defaults as d


class Gui:
    def new_menu_item(self, name, img=None, accel=None, func=None, *args):
        if img is not None:
            menu_item = gtk.ImageMenuItem(img, name)
            key, mod = gtk.accelerator_parse(accel)
            menu_item.add_accelerator('activate', self.shortcuts, key, mod, gtk.ACCEL_VISIBLE)
        elif name == 'sep':
            menu_item = gtk.SeparatorMenuItem()
        else:
            menu_item = gtk.MenuItem(name)

        if func is not None:
            menu_item.connect('activate', func, name)

        menu_item.show()
        return menu_item

    def create_menu(self):
        self.shortcuts = gtk.AccelGroup()
        self.window.add_accel_group(self.shortcuts)

        file_root = gtk.MenuItem('File')
        file_items = [['New',    gtk.STOCK_NEW,      '<Control>N',       self.new_file],
                      ['Open',   gtk.STOCK_OPEN,     '<Control>O',       self.open_file],
                      ['Save As',gtk.STOCK_SAVE_AS,  '<Control><Shift>S',self.new_file],
                      ['Save',   gtk.STOCK_SAVE,     '<Control>S',       self.save_file],
                      ['sep',    None,               None,               None],
                      ['Quit',   gtk.STOCK_QUIT,     '<Control>Q',       self.delete_event]]
        file_menu = gtk.Menu()
        file_root.set_submenu(file_menu)
        for name, img, accel, func in file_items:
            menu_item = self.new_menu_item(name, img, accel, func)
            file_menu.append(menu_item)
        file_root.show()
        file_menu.show()

        newobj_root = gtk.MenuItem('Objects')
        newobj_items = [['Create new modulator', self.new_modulator]]
        newobj_menu = gtk.Menu()
        newobj_root.set_submenu(newobj_menu)
        for name, func in newobj_items:
            menu_item = self.new_menu_item(name, func=func)
            newobj_menu.append(menu_item)
        newobj_root.show()
        newobj_menu.show()

        self.menu_separator = gtk.VBox()
        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.add_with_viewport(self.menu_separator)
        self.window.add(self.scrolled_window)
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC,
                                        gtk.POLICY_AUTOMATIC)  # make the scrollbars show only when needed
        self.scrolled_window.show()
        self.menu_separator.show()

        self.menu_bar = gtk.MenuBar()
        self.menu_separator.pack_start(self.menu_bar, False, False, 2)
        self.menu_bar.append(file_root)
        self.menu_bar.append(newobj_root)
        self.menu_bar.show()

        key_items = [['Edit CC number...', self.edit_key_attrs],
                     ['Edit key function...', self.edit_key_attrs],
                     ['Edit key colour...', self.edit_key_attrs],
                     ['Link to modulator...', self.edit_key_attrs]]
        self.key_menu = gtk.Menu()
        for name, func in key_items:
            menu_item = self.new_menu_item(name, func=func)
            self.key_menu.append(menu_item)

    def create_pot_widgs(self):
        for y in range(d.NUM_OF_POTS_V):
            self.pot_widgs.append([])
            for x in range(d.NUM_OF_POTS_H):
                parent = engine.pots[y][x]
                self.pot_widgs[y].append(PotWidg(parent, engine))
                cur_widg = self.pot_widgs[y][x]
                self.pot_grid.attach(cur_widg.alignment, x, x+1, y, y+1)

    def create_key_widgs(self):
        for y in range(d.NUM_OF_KEYS_V):
            self.key_widgs.append([])
            for x in range(d.NUM_OF_KEYS_V):
                parent = engine.keys[y][x]
                self.key_widgs[y].append(KeyWidg(parent, engine))
                cur_widg = self.key_widgs[y][x]
                self.key_grid.attach(cur_widg.alignment, x, x+1, y, y+1)

    def refresh_widgets(self):
        for i, row in enumerate(self.key_widgs):
            for j, key_widg in enumerate(row):
                key_widg.set_parent(engine.keys[i][j])

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('TopHat MIDI')
        self.window.set_default_size(800, 600)
        self.window.connect('delete_event', self.delete_event)
        self.create_menu()
        self.widget_separator = gtk.HBox()
        self.pot_widgs = []
        self.key_widgs = []
        self.pot_grid = gtk.Table(d.NUM_OF_POTS_H, d.NUM_OF_POTS_V)
        self.key_grid = gtk.Table(d.NUM_OF_KEYS_H, d.NUM_OF_KEYS_V)
        self.create_pot_widgs()
        self.create_key_widgs()
        self.widget_separator.pack_start(self.pot_grid)
        self.widget_separator.pack_start(self.key_grid)
        self.menu_separator.pack_start(self.widget_separator)
        self.pot_grid.show()
        self.key_grid.show()
        self.widget_separator.show()
        self.menu_separator.show()
        self.window.show()

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def new_file(self, widget, event, data=None):
        if event == 'New':
            title = 'Create a new file'
            func = engine.new_file
        elif event == 'Save As':
            title = 'Save as'
            func = engine.save_as
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
            func(filename_input.get_text(), new_file_window.get_filename())
            self.refresh_widgets()
        new_file_window.destroy()
        self.window.queue_draw()

    def open_file(self, widget, event, data=None):
        open_file_window = gtk.FileChooserDialog(title='Select a file to open',
                                                 parent=self.window,
                                                 buttons=(gtk.STOCK_CANCEL,
                                                          gtk.RESPONSE_CANCEL,
                                                          gtk.STOCK_OPEN,
                                                          gtk.RESPONSE_OK))
        event = open_file_window.run()
        if event == gtk.RESPONSE_OK:
            engine.open(open_file_window.get_filename())
            self.refresh_widgets()
        open_file_window.destroy()

    def save_file(self, widget, event, data=None):
        engine.save()

    def new_modulator(self, **kwargs):  # TODO: actually make this function. Should create a new mod_widg on the screen.
        pass

    def entry_control(self, entry, event, key_widg):
        if event.type == gtk.gdk._2BUTTON_PRESS:
            entry.set_editable(True)
            entry.set_has_frame(True)
            entry.grab_focus()
            entry.select_region(0, -1)
        elif event.type == gtk.gdk.BUTTON_PRESS:
            entry.set_position(0)
        else:
            normalise = False
            if event.type == gtk.gdk.FOCUS_CHANGE:
                normalise = True
            # elif event.type == gtk.gdk.KEY_PRESS:
            #     if event.keyval == 65293:  # enter was pressed
            #         normalise = True
            if normalise:
                entry.set_editable(False)
                entry.set_has_frame(False)
                key_widg.parent.set_name(entry.get_text())
                entry.select_region(0, 0)
        return True

    def edit_key_attrs(self, menu, event, data=None):
        active_key = self.selected_key_widg.parent
        if event == 'Edit CC number...':
            prev_val = active_key.midi_loc
            func = active_key.set_midi_loc
        elif event == 'Edit key function...':
            prev_val = active_key.func
            func = active_key.set_func
        elif event == 'Edit key colour...':
            prev_val = active_key.colour
            func = active_key.set_colour
        else:  # event == 'Link to modulator...':
            prev_val = active_key.linked_mod
            func = active_key.set_linked_mod

        entry = EntryDialog(parent=None,
                            flags=gtk.DIALOG_DESTROY_WITH_PARENT,
                            message_format=event,  # the title of the entry dialog
                            buttons=gtk.BUTTONS_OK,
                            default_value=prev_val)
        entry.format_secondary_text('Please enter a new value')
        new_val = entry.run()
        if new_val is not None:
            func(new_val)  # call the function specified above with the new value to be set
        entry.destroy()


if __name__ == "__main__":
    engine = Engine()
    engine.new_file('default', 'C:\\Users\\Celery\\Documents\\TopHat-MIDI')
    engine.open('C:\\Users\\Celery\\Documents\\TopHat-MIDI\\default.txt')
    gui = Gui()
    gtk.main()