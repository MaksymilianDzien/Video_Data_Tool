from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import QRect, QRectF, QPoint


class Draw_rectangle:

    # Color of rectangle
    Color_of_rectange = QColor(255, 0, 0)  #red rgb change in future

    # Drawing Alpha
    alpha = 60

    #wiget image for images and annocation labes
    def __init__(self, widget_image, Label_log):

        # init widget
        self.widget_image = widget_image

        # set default annotaios label
        self.Label_log = Label_log

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

    # hander of mouse press - start of drawing (first point)
    def mouse_press_handler(self, point_posstion):

        if not self.set_draw_enabled:
            return

        # set first point of rectangle
        self.mouse_first_point = QPoint(point_posstion)
        # set current point same as first - so preview rectangle can draw immediately
        self.mouse_current_point = QPoint(point_posstion)

    # hander of mouse release - end of drawing
    def mouse_release_handler(self, point_posstion, curent_index_frame):

        #chek if enable
        if not self.set_draw_enabled or self.mouse_first_point is None:
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

        # add annotation to frame
        if curent_index_frame not in self.fream_annotation:
            self.fream_annotation[curent_index_frame] = []

        #scaling rectange if zomm is not 1
        scale_current_rectangle = self.convert_rectangle_to_current_scale(curent_rectangle)

        # annotation info
        new_annotation = \
            {
                "rect": scale_current_rectangle,
                "label": ""
            }
        self.fream_annotation[curent_index_frame].append(new_annotation)

        # draw rectangle
        self.widget_image.update()


        #  create new or set laves (fuction in label_log)
        label_rectangle_text, ok_input = self.Label_log.choose_annotation_label_option(self.widget_image)

        # chek if press ok_input o or is not label
        if not ok_input or not label_rectangle_text:

            # user cancelled anntaion
            self.fream_annotation[curent_index_frame].remove(new_annotation)
            self.widget_image.update()
            return

        #set name off addnotaion
        new_annotation["label"] = label_rectangle_text
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

            # calculate and scale recatangle (zoom)
            current_scaled_rectangle = self.convert_all_rectangle_to_scale(rect)

            rectangle_painter.drawRect(current_scaled_rectangle)

            # add label to rataongle top right coner
            # cs
            if label:
                rectangle_painter.drawText(current_scaled_rectangle.topLeft().x(), current_scaled_rectangle.topLeft().y() - 5, label)

        # drawing ratangle before set secont point
        if self.mouse_first_point is not None and self.mouse_current_point is not None:
            rectangle_drawing_shape = QRect(self.mouse_first_point, self.mouse_current_point).normalized()
            rectangle_painter.drawRect(rectangle_drawing_shape)

    # convert to base scale
    #if is new createt and calucate current off set and sacle in this crectangle
    def convert_rectangle_to_current_scale(self, base_screen_coordintates_rectangle):

        #scale
        current_zoom_level = self.widget_image.zoom_level

        #image pozition
        current_image_postion = self.widget_image.positon

        #set true postion of rectangle (no scale no offset)
        return QRectF(
            #x coranatie = coordintates rectangle - offset / scale
            (base_screen_coordintates_rectangle.x() - current_image_postion.x()) / current_zoom_level,
            #y coranatie = coordintates rectangle  - offset / scale
            (base_screen_coordintates_rectangle.y() - current_image_postion.y()) / current_zoom_level,
            # width = current width / scale
            base_screen_coordintates_rectangle.width() / current_zoom_level,
            # height = current height / scale
            base_screen_coordintates_rectangle.height() / current_zoom_level
        )


    #convert all rectangle in screen
    #
    def convert_all_rectangle_to_scale(self, screen_scaled_coordintates_rectangle):

        # scale
        current_zoom_level = self.widget_image.zoom_level
        # image pozition
        current_image_postion = self.widget_image.positon

        return QRect(
            # x = curent_x * scale + offset
            round(screen_scaled_coordintates_rectangle.x() * current_zoom_level + current_image_postion.x()),
            # y = curent_y * scale + offset
            round(screen_scaled_coordintates_rectangle.y() * current_zoom_level + current_image_postion.y()),
            # width = = current width * zoom
            round(screen_scaled_coordintates_rectangle.width() * current_zoom_level),
            # height = = current height * zoom
            round(screen_scaled_coordintates_rectangle.height() * current_zoom_level)
        )