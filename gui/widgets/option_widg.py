__author__ = 'Celery'

import gtk
from base_widg import BaseWidg
import midi.defaults.defaults as d


class OptionWidg(BaseWidg):
    def __init__(self, linked_widg):
        self.lnkd_widg = linked_widg
        lwp = self.lnkd_widg.get_parent()
        self.alignment = gtk.Alignment()
        self.frame = gtk.Frame()
        if lwp.__class__.__name__ == 'Pot':
            option_menu_y = d.OPTION_MENU_Y + 1
        else:
            option_menu_y = d.OPTION_MENU_Y

        self.table = gtk.Table(d.OPTION_MENU_X, option_menu_y)
        self.labels = [gtk.Label() for i in range(option_menu_y)]
        self.entries = [gtk.Entry() for i in range(option_menu_y - 1)]
        self.combo_box = gtk.combo_box_new_text()

        self.frame.set_size_request(d.OPTION_WIDGET_WIDTH, d.DEFAULT_WIDGET_HEIGHT)
        self.alignment.set(0.5, 0.5, 0, 0)  # centrally align everything inside

        label_data = ['Name:',
                      'CC no:',
                      'Colour:',
                      'Func:']
        if lwp.__class__.__name__ == 'Pot':
            label_data.insert(3, 'Steps:')
        for i, label in enumerate(self.labels):
            label.set_text(label_data[i])
            label.set_alignment(xalign=1.0, yalign=0.5)
            self.table.attach(label, 0, 1, i, i + 1, xpadding=d.OPTION_PADDING)
        self.update_text()
        for i, entry in enumerate(self.entries):
            self.table.attach(entry, 1, 2, i, i + 1, gtk.SHRINK | gtk.FILL, xpadding=d.OPTION_PADDING)
        self.combo_box.connect('changed', self.combo_callback, lwp.set_func)
        if lwp.__class__.__name__ == 'Pot':
            combo_y_pos = [4, 5]
        else:
            combo_y_pos = [3, 4]
        self.table.attach(self.combo_box, 1, 2, combo_y_pos[0], combo_y_pos[1], gtk.SHRINK | gtk.FILL, gtk.SHRINK, d.OPTION_PADDING)
        for func in lwp.get_available_funcs():
            self.combo_box.append_text(func)
        self.combo_box.set_active(lwp.get_available_funcs().index(lwp.func))
        self.frame.add(self.table)
        self.alignment.add(self.frame)
        self.show_self()
        self.set_visibility(False)

    def update_text(self):
        lwp = self.lnkd_widg.get_parent()
        entry_data = [(lwp.get_name(), lwp.set_name, ('name', self.lnkd_widg.label)),
              (lwp.get_midi_loc(), lwp.set_midi_loc, ('cc no')),
              (lwp.get_colour(), lwp.set_colour, ('colour', self.lnkd_widg.fill))]
        if lwp.__class__.__name__ == 'Pot':
            entry_data.append((lwp.get_num_steps(), lwp.set_num_steps, ('steps')))
        for i, entry in enumerate(self.entries):
            entry.set_text(str(entry_data[i][0]))
            entry.connect('activate', self.entry_callback, entry_data[i][1], entry_data[i][2])

    @staticmethod
    def entry_callback(widget, function, args):
        text = widget.get_text()
        function(text)
        if args[0] == 'name':  # dynamically setting functions results in things like this:
            args[1].set_text(text)  # in order for set_name to work, it needs extra bits of data no other callback needs
        elif args[0] == 'colour':  # so args[1] is out of range when args[0] is 'midi' as it doesn't need anything extra
            args[1]()  # set the new colour immediately, don't wait for redraw

    @staticmethod
    def combo_callback(widget, function):
        text = widget.get_active_text()
        function(text)