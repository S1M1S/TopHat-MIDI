__author__ = 'Celery'


class KeyWidg:
    def __init__(self, parent, align, frame, h_box, key_box, drawing_area, entry, x_loc, y_loc):
        self.parent = parent
        self.frame = frame
        self.align = align
        self.h_box = h_box
        self.key_box = key_box
        self.drawing_area = drawing_area
        self.entry = entry
        self.x_loc = x_loc
        self.y_loc = y_loc

    def create_option_menu(self, opt_frame, opt_table, opt_name, opt_cc_num, opt_colour, opt_func):
        self.opt_frame = opt_frame
        self.opt_table = opt_table
        self.opt_name_lbl, self.opt_name = opt_name
        self.opt_cc_num_lbl, self.opt_cc_num = opt_cc_num
        self.opt_colour_lbl, self.opt_colour = opt_colour
        self.opt_func_lbl, self.opt_func = opt_func

    def set_parent(self, new_parent):
        self.parent = new_parent