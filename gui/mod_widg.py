__author__ = 'Celery'


class ModWidg:
    def __init__(self, parent, align, frame, box, drawing_area, entry, x_loc, y_loc):
        self.parent = parent
        self.frame = frame
        self.align = align
        self.box = box
        self.drawing_area = drawing_area
        self.entry = entry
        self.x_loc = x_loc
        self.y_loc = y_loc

    def set_parent(self, new_parent):
        self.parent = new_parent