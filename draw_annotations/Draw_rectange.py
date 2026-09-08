from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import QRect, QPoint


class Draw_rectangle:

    # Color of rectangle
    Color_of_rectange = QColor(255, 0, 0)  #red rgb

    # Drawing Alpha
    alpha = 60

    def __init__(self, widget_image):

        # init widget
        self.widget_image = widget_image

        # init annotations per frame
        self.fream_annotation = {}

        # set draw
        self.set_draw_enabled = False

        # set first point
        self.mouse_first_point = None

        # set mouse positon
        self.mouse_current_point = None

    # enable/unenable drawing
    def draw_mod_enable(self, is_enable):

        self.set_draw_enabled = is_enable

        # if rectange is not complete set to
        self.mouse_first_point = None
        self.mouse_current_point = None

    #hander of current click points
    def click_handler(self, point_posstion, curent_index_frame):

        if not self.set_draw_enabled:
            return

        # set first point of rectangle
        if self.mouse_first_point is None:
            self.mouse_first_point = QPoint(point_posstion)
            return

        # set second point of rectangle
        mouse_second_point = QPoint(point_posstion)
        curent_rectangle = QRect(self.mouse_first_point, mouse_second_point).normalized()

        # reset points
        self.mouse_first_point = None
        self.mouse_current_point = None

        # to small rectangle return
        if curent_rectangle.width() < 3 or curent_rectangle.height() < 3:
            self.widget_image.update()
            return

        # create and set label
        label_rectangle_text, ok_input = (QInputDialog.getText( self.widget_image, "New label", "Enter label name:"))

        # chek if press ok_input o or is not label
        if not ok_input or not label_rectangle_text:
            self.widget_image.update()
            return

        # add annotation to frame
        if curent_index_frame not in self.fream_annotation:
            self.fream_annotation[curent_index_frame] = []

        # annotation info
        (self.fream_annotation[curent_index_frame].append
            ({
            "rect": curent_rectangle,
            "label": label_rectangle_text
            }))

        self.widget_image.update()

    # drawing retangle wvie
    def mouse_move_handle(self, point_posstion):

        #check if draw is enable and is set first mouse point
        if not self.set_draw_enabled or self.mouse_first_point is None:
            return

        #ser mouse point
        self.mouse_current_point = QPoint(point_posstion)
        self.widget_image.update()

    # draw all annotainon in frame
    def draw_rectangle_annotation(self, rectangle_painter, curent_frame_index):

        #set rectaongle perimeter
        rectangle_pen = QPen(self.Color_of_rectange)
        #set color of  perimeter
        rectangle_pen.setWidth(2)
        rectangle_painter.setPen(rectangle_pen)

        #set fill color of rectangle
        rectangle_fill_color = QColor(self.Color_of_rectange)
        rectangle_fill_color.setAlpha(self.alpha)
        rectangle_painter.setBrush(QBrush(rectangle_fill_color))

        # add annotations to frame
        all_annotations_frame = self.fream_annotation.get(curent_frame_index, [])

        #adding annotanions
        for curent_annotation in all_annotations_frame:
            rect = curent_annotation["rect"]
            label = curent_annotation["label"]

            rectangle_painter.drawRect(rect)
            # add label to rataongle top right coner
            rectangle_painter.drawText(rect.topLeft().x(), rect.topLeft().y() - 5, label)

        # drawing ratangle before set secont point
        if self.mouse_first_point is not None and self.mouse_current_point is not None:
            rectangle_drawing_shape = QRect(self.mouse_first_point, self.mouse_current_point).normalized()
            rectangle_painter.drawRect(rectangle_drawing_shape)