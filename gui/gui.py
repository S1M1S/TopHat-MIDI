__author__ = 'Celery'

import pygtk
pygtk.require('2.0')
import gtk
from midi.main import Engine
from key_widg import KeyWidg
from pot_widg import PotWidg
from mod_widg import ModWidg
import midi.defaults as d


class EntryDialog(gtk.MessageDialog):  # a class I found on stackoverflow - from user FriendFX
    def __init__(self, *args, **kwargs):
        '''
        Creates a new EntryDialog. Takes all the arguments of the usual
        MessageDialog constructor plus one optional named argument
        "default_value" to specify the initial contents of the entry.
        '''
        if 'default_value' in kwargs:
            default_value = kwargs['default_value']
            del kwargs['default_value']
        else:
            default_value = ''
        super(EntryDialog, self).__init__(*args, **kwargs)
        entry = gtk.Entry()
        entry.set_text(str(default_value))
        entry.connect("activate",
                      lambda ent, dlg, resp: dlg.response(resp),
                      self, gtk.RESPONSE_OK)
        self.vbox.pack_end(entry, True, True, 0)
        self.vbox.show_all()
        self.entry = entry
    def set_value(self, text):
        self.entry.set_text(text)
    def run(self):
        result = super(EntryDialog, self).run()
        if result == gtk.RESPONSE_OK:
            text = self.entry.get_text()
        else:
            text = None
        return text


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
        self.window.add(self.menu_separator)
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

    def create_key_visual_components(self):
        for i, row in enumerate(self.key_widgs):
            for j, cell in enumerate(row):
                self.key_widgs[i][j] = KeyWidg(
                    engine.keys[i][j],
                    gtk.Alignment(),
                    gtk.Frame(),
                    gtk.VBox(),
                    gtk.DrawingArea(),
                    gtk.Entry(),
                    i,
                    j
                )

    def create_key_widgets(self):
        self.key_grid = gtk.Table(d.NUM_OF_KEYS_H , d.NUM_OF_KEYS_V)
        for i, row in enumerate(self.key_widgs):
            for j, key_widg in enumerate(row):
                key_widg.align.set(0.5, 0.5, 0, 0)
                key_widg.box.set_size_request(d.KEY_AREA_H, d.KEY_AREA_V+21)
                key_widg.drawing_area.set_size_request(d.KEY_AREA_H, d.KEY_AREA_V)
                key_widg.drawing_area.set_events(gtk.gdk.EXPOSURE_MASK
                                                | gtk.gdk.BUTTON_PRESS_MASK
                                                | gtk.gdk.BUTTON_RELEASE_MASK)  # drawing areas do not receive mouse clicks by default
                key_widg.entry.set_text(key_widg.parent.name)
                key_widg.entry.set_editable(False)
                key_widg.entry.set_has_frame(False)
                key_widg.entry.set_max_length(d.MAX_NAME_LENGTH)
                key_widg.entry.set_alignment(0.5)

                key_widg.box.pack_start(key_widg.drawing_area)
                key_widg.box.pack_end(key_widg.entry)
                key_widg.align.add(key_widg.frame)
                key_widg.frame.add(key_widg.box)
                key_widg.entry.show()
                key_widg.box.show()
                key_widg.frame.show()
                key_widg.align.show()
                self.key_grid.attach(key_widg.align, key_widg.x_loc, key_widg.x_loc+1, key_widg.y_loc, key_widg.y_loc+1)

                key_widg.drawing_area.connect('expose_event', self.draw_key_widgets, key_widg)
                key_widg.drawing_area.connect('button_release_event', self.key_control, key_widg)
                key_widg.drawing_area.connect('button_press_event', self.key_control, key_widg)
                key_widg.entry.connect('button_press_event', self.entry_control, key_widg)
                # key_widg.entry.connect('key_press_event', self.entry_control, key_widg)
                key_widg.entry.connect('focus_out_event', self.entry_control, key_widg)

    def draw_key_widgets(self, key_drawing_area, event, key_widg):
        key_drawable = key_drawing_area.window
        key_drawable.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
        context = key_drawable.new_gc()
        colour_map = key_drawing_area.get_colormap()
        context.set_values(foreground=colour_map.alloc('white'))
        key_drawable.draw_rectangle(context, True, 0, 0, d.KEY_AREA_H, d.KEY_AREA_V)
        context.set_values(foreground=colour_map.alloc('grey'), line_width=6, cap_style=gtk.gdk.CAP_ROUND, join_style=gtk.gdk.JOIN_ROUND)
        key_drawable.draw_rectangle(context, False, 10, 10, 80, 80)
        if key_widg.parent.state:  # willed be filled according to its state of activation
            r, g, b = key_widg.parent.get_gtk_colour()
            context.set_values(foreground=colour_map.alloc(r, g, b))
            key_drawable.draw_rectangle(context, True, 10+3, 10+3, 80-6, 80-6)
        return True

    def refresh_key_widgets(self):
        for i, row in enumerate(self.key_widgs):
            for j, key_widg in enumerate(row):
                key_widg.set_parent(engine.keys[i][j])

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('TopHat MIDI')
        self.window.set_size_request(800, 600)
        self.window.connect('delete_event', self.delete_event)
        self.create_menu()
        self.key_widgs = [[None]*d.NUM_OF_KEYS_H for i in range(d.NUM_OF_KEYS_V)]
        self.create_key_visual_components()
        self.create_key_widgets()
        for row in self.key_widgs:
            for key_widg in row:
                key_widg.drawing_area.show()
        self.key_grid.show()
        self.menu_separator.pack_start(self.key_grid)
        self.window.show()

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

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
            engine.new_file(filename_input.get_text(), new_file_window.get_filename())
            self.refresh_key_widgets()
        new_file_window.destroy()
        self.window.queue_draw()

    def open_file(self, widget, event, data=None):
        open_file_window = gtk.FileChooserDialog(title='Select a file to open',
                                                 parent=self.window,
                                                 buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        event = open_file_window.run()
        if event == gtk.RESPONSE_OK:
            engine.open(open_file_window.get_filename())
            self.refresh_key_widgets()
        open_file_window.destroy()

    def save_file(self, widget, event, data=None):
        engine.save()

    def new_modulator(self, **kwargs):  # TODO: actually make this function. Should create a new mod_widg on the screen.
        pass

    def key_control(self, key_drawing_area, event, key_widg):
        if event.type == gtk.gdk.BUTTON_PRESS:
            if event.button == 1:
                if key_widg.parent.set_state('press'):
                    engine.midi_out(key_widg.parent.midi_loc, key_widg.parent.get_midi_vel())
                key_drawing_area.queue_draw()
            else:
                self.selected_key_widg = key_widg  # so we know whose settings we are changing
                self.key_menu.popup(None, None, None, event.button, event.time)  # give a context menu
        elif event.type == gtk.gdk.BUTTON_RELEASE:
            key_widg.parent.set_state('release')
            key_drawing_area.queue_draw()
        return True

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
            func = active_key.set_funcc
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
    engine.open('C:\\Users\\Celery\\Documents\\TopHat-MIDI\\default.txt')
    gui = Gui()
    gtk.main()