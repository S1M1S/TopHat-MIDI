__author__ = 'Celery'

import pygtk
pygtk.require('2.0')
import gtk
from midi.main import Engine
from midi.key import Key
from midi.pot import Pot
import midi.defaults as default


class KeyEle():
    def __init__(self, parent, align, frame, box, drawing_area, entry, x_loc, y_loc):
        self.parent = parent
        self.frame = frame
        self.align = align
        self.box = box
        self.drawing_area = drawing_area
        self.entry = entry
        self.x_loc = x_loc
        self.y_loc = y_loc


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

    def create_key_widgets(self):
        self.key_grid = gtk.Table(default.NUM_OF_KEYS_H , default.NUM_OF_KEYS_V)
        for row in self.key_eles:
            for key_ele in row:
                key_ele.align.set(0.5, 0.5, 0, 0)
                key_ele.box.set_size_request(default.KEY_AREA_H, default.KEY_AREA_V+21)
                key_ele.drawing_area.set_size_request(default.KEY_AREA_H, default.KEY_AREA_V)
                key_ele.drawing_area.set_events(gtk.gdk.EXPOSURE_MASK
                                                | gtk.gdk.BUTTON_PRESS_MASK
                                                | gtk.gdk.BUTTON_RELEASE_MASK)  # drawing areas do not recieve mouseclicks by default
                key_ele.drawing_area.connect('expose_event', self.draw_key_widgets, key_ele)
                key_ele.drawing_area.connect('button_release_event', self.key_control, key_ele)
                key_ele.drawing_area.connect('button_press_event', self.key_control, key_ele)

                key_ele.entry.set_text(key_ele.parent.name)
                key_ele.entry.set_editable(False)
                key_ele.entry.set_has_frame(False)
                key_ele.entry.set_max_length(default.MAX_NAME_LENGTH)
                key_ele.entry.set_alignment(0.5)
                key_ele.entry.connect('button_press_event', self.entry_control, key_ele)
                # key_ele.entry.connect('key_press_event', self.entry_control, key_ele)
                key_ele.entry.connect('focus_out_event', self.entry_control, key_ele)

                key_ele.box.pack_start(key_ele.drawing_area)
                key_ele.box.pack_end(key_ele.entry)
                key_ele.align.add(key_ele.frame)
                key_ele.frame.add(key_ele.box)
                key_ele.entry.show()
                key_ele.box.show()
                key_ele.frame.show()
                key_ele.align.show()

                self.key_grid.attach(key_ele.align, key_ele.x_loc, key_ele.x_loc+1, key_ele.y_loc, key_ele.y_loc+1)

    def draw_key_widgets(self, key_drawing_area, event, key_ele):
        key_drawable = key_drawing_area.window
        key_drawable.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
        context = key_drawable.new_gc()
        colour_map = key_drawing_area.get_colormap()
        context.set_values(foreground=colour_map.alloc('white'))
        key_drawable.draw_rectangle(context, True, 0, 0, default.KEY_AREA_H, default.KEY_AREA_V)
        context.set_values(foreground=colour_map.alloc('grey'), line_width=6, cap_style=gtk.gdk.CAP_ROUND, join_style=gtk.gdk.JOIN_ROUND)
        key_drawable.draw_rectangle(context, False, 10, 10, 80, 80)  # rect will be filled according to key.state
        if key_ele.parent.state:
            r, g, b = key_ele.parent.get_gtk_colour()
            context.set_values(foreground=colour_map.alloc(r, g, b))
            key_drawable.draw_rectangle(context, True, 10+3, 10+3, 80-6, 80-6)

        return True

    def key_control(self, key_drawing_area, event, key_ele):
        if event.type == gtk.gdk.BUTTON_PRESS:
            key_ele.parent.set_state('press')
            key_drawing_area.queue_draw()
        elif event.type == gtk.gdk.BUTTON_RELEASE:
            key_ele.parent.set_state('release')
            key_drawing_area.queue_draw()
        return True

    def entry_control(self, entry, event, key_ele):
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
                key_ele.parent.set_name(entry.get_text())
                entry.select_region(0, 0)

        return True

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('TopHat MIDI')
        self.window.set_size_request(250, 200)
        self.window.connect('delete_event', self.delete_event)
        self.create_menu()
        self.key_eles = [[None]*default.NUM_OF_KEYS_H for i in range(default.NUM_OF_KEYS_V)]
        for i in range(default.NUM_OF_KEYS_H):
            for j in range(default.NUM_OF_KEYS_V):
                self.key_eles[i][j] = KeyEle(
                    engine.keys[i][j],
                    gtk.Alignment(),
                    gtk.Frame(),
                    gtk.VBox(),
                    gtk.DrawingArea(),
                    gtk.Entry(),
                    i,
                    j
                )
        self.create_key_widgets()
        self.menu_separator.pack_start(self.key_grid)
        for row in self.key_eles:
            for key_ele in row:
                key_ele.drawing_area.show()
        self.key_grid.show()
        self.window.show()
        self.window.connect('notify::is-active', self.printer)

    def printer(self):
        print 's'

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

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False


if __name__ == "__main__":
    engine = Engine()
    engine.open('C:\\Users\\Celery\\Documents\\TopHat-MIDI\\default.txt')
    gui = Gui()
    gtk.main()
