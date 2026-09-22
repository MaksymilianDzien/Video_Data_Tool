import math
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import QPoint, QPointF, QRectF


class Edit_annotation:

    # size of handler
    corner_size_of_hander = 10
    rotate_of_hander = 6
    rotate_offset = 30

    # clor handler
    color_of_hander = QColor(0, 150, 255)

    def __init__(self, current_widget_image, draw_current_rectangle):

        # widget image  (ButtonLogic)
        self.current_widget_image = current_widget_image

        # set rectangle logick
        self.draw_rectangle = draw_current_rectangle

        # set edit eanable
        self.edit_of_annotation = False

        # current  selected annotation and frame index ( table )
        self.select_current_annotation = None
        self.select_curennt_frame_index = None

        #current actiateted handler rigth top ... dow right or none
        self.select_actived_hander = None


        # coppy of rectangle of sate referenc
        self.drag_start_of_rectangle = None

    # enable/unenable  edit of anntotaion
    def enable_edited_mode(self, enabled):

        self.edit_of_annotation = enabled

        if not enabled:
            self.deselecte_edited_mode()

    # disable edited mod if is new frame or new button is clicet or new flie
    def deselecte_edited_mode(self):

        self.select_current_annotation = None
        self.select_curennt_frame_index = None
        self.select_actived_hander = None
        self.drag_start_of_rectangle = None

    # rectangle after calkulated zomm and rotate
    def get_current_annotation_rectangle(self, annotation):
        base_rectangle = self.draw_rectangle.build_rectangle_for_annotation_info(annotation)
        return self.draw_rectangle.convert_all_rectangle_to_scale(base_rectangle)

    # rotate current annotaion
    def rotate_around_center_point(self, current_point, annotation_center, angle_degrees):

        #angle radnants
        radians = math.radians(angle_degrees)

        #delta points
        delta_x = current_point.x() - annotation_center.x()
        delta_y = current_point.y() - annotation_center.y()

        #rorated x and y
        rotate_x = delta_x * math.cos(radians) - delta_y * math.sin(radians)
        rotate_y = delta_x * math.sin(radians) + delta_y * math.cos(radians)

        return QPoint(round(rotate_x + annotation_center.x()), round(rotate_y + annotation_center.y()))


    # screen potin to primary
    def screen_points_to_primary_points(self, current_screen_point):

        screen_zoom_level = self.current_widget_image.base_zoom_level
        screen_image_offset = self.current_widget_image.positon

        return QPointF(
            (current_screen_point.x() - screen_image_offset.x()) / screen_zoom_level,
            (current_screen_point.y() - screen_image_offset.y()) / screen_zoom_level
        )

    # 4 logical handler of annotation
    def get_primary_corners_of_hander(self, screen_rect):
        return {
            "top_left": screen_rect.topLeft(),
            "top_right": screen_rect.topRight(),
            "bottom_left": screen_rect.bottomLeft(),
            "bottom_right": screen_rect.bottomRight()
        }

    # chek if find hander
    def find_hander_press(self, point_posstion):

        #if annotation is not selected
        if self.select_current_annotation is None:
            return None

        #download all  rectangle
        screen_rectangle = self.get_current_annotation_rectangle(self.select_current_annotation)

        #download center of rectangle
        annotation_center = screen_rectangle.center()

        #download rotation of rectangle
        annotation_rotation = self.select_current_annotation["rotation"]

        # main rotate hander not rotated
        logical_rotate_hander = QPoint(screen_rectangle.center().x(), screen_rectangle.top() - self.rotate_offset)

        # rotate hander after
        visual_rotate_hander = self.rotate_around_center_point(logical_rotate_hander, annotation_center, annotation_rotation)

        # rotated distanece fo hander sqrt(a2 +b2)
        distance_rotated_hander = math.hypot(

            point_posstion.x() - visual_rotate_hander.x(),
            point_posstion.y() - visual_rotate_hander.y()
        )

        #if distace is too small
        if distance_rotated_hander <= self.rotate_of_hander + 4:
            return "rotate"

        # get all logical corrners
        logical_hander_corners = self.get_primary_corners_of_hander(screen_rectangle)

        #rotate all corrners
        for handle_name, logical_corner in logical_hander_corners.items():
            visual_corner = self.rotate_around_center_point(logical_corner, annotation_center, annotation_rotation)

            #too small Wreturn corrner name
            if abs(point_posstion.x() - visual_corner.x()) <= self.corner_size_of_hander \
                    and abs(point_posstion.y() - visual_corner.y()) <= self.corner_size_of_hander:
                return handle_name

        return None

    # chek if point is in anotation
    def is_point_in_rotated_anotation(self, point_posstion, annotation):

        # download center of rectangle
        screen_rectangle = self.get_current_annotation_rectangle(annotation)

        # download rotation of rectangle
        annotation_center = screen_rectangle.center()

        #get center local point of anotation
        local_point = self.rotate_around_center_point(point_posstion, annotation_center, -annotation["rotation"])

        return screen_rectangle.contains(local_point)


    def mouse_press_hander(self, point_posstion, curent_index_frame):

        # if eidt is not enable
        if not self.edit_of_annotation:
            return

        # chek if hander is selected
        if self.select_current_annotation is not None and self.select_curennt_frame_index == curent_index_frame:

            #save current hander preset
            handle_name = self.find_hander_press(point_posstion)

            if handle_name is not None:

                # what hander is actived
                self.select_actived_hander = handle_name

                #main rectangle to reference
                self.drag_start_of_rectangle = self.draw_rectangle.build_rectangle_for_annotation_info(self.select_current_annotation)
                return

        # if hander is not clicked then chek if clicked in annotation itself
        frame_annotations = self.draw_rectangle.fream_annotation.get(curent_index_frame, [])

        # end of list all annotations fresh annotations in top list
        for annotation in reversed(frame_annotations):
            if self.is_point_in_rotated_anotation(point_posstion, annotation):
                self.select_current_annotation = annotation
                self.select_curennt_frame_index = curent_index_frame
                self.select_actived_hander = None
                self.current_widget_image.update()
                return

        # miss or not select any annotations disable edit annotations and update current image
        self.deselecte_edited_mode()
        self.current_widget_image.update()

    def mouse_move_hander(self, point_posstion):

        # if is not enable or is not selectet or is not active
        if not self.edit_of_annotation or self.select_actived_hander is None or self.select_current_annotation is None:
            return

        #if rotate hander is selected
        if self.select_actived_hander == "rotate":
            self.update_annotation_rotation(point_posstion)
        # if any else hander is selected
        else:
            self.update_annotation_resize(point_posstion)

        #update image to see change
        self.current_widget_image.update()

    def mouse_release_hander(self):

        #if edit is enable or is not selected
        if not self.edit_of_annotation or self.select_actived_hander is None:
            return

        #delete flag to actived hander and referec to rectangle
        self.select_actived_hander = None
        self.drag_start_of_rectangle = None

        # save current stage of rectangle to undo list
        self.draw_rectangle.on_annotion_comit()


    # upade annotation in drag mouse clik
    def update_annotation_rotation(self, point_posstion):

        # set main center rotate point
        screen_rectangle = self.draw_rectangle.convert_all_rectangle_to_scale(self.drag_start_of_rectangle)
        annotation_center = screen_rectangle.center()

        # delta points
        delta_x = point_posstion.x() - annotation_center.x()
        delta_y = point_posstion.y() - annotation_center.y()

        # delta angle
        angle_degrees = math.degrees(math.atan2(delta_x, -delta_y))

        #save current annotation rotation
        self.select_current_annotation["rotation"] = angle_degrees % 360

    # update selected hander
    def update_annotation_resize(self, point_posstion):

        # set main center rotate point
        screen_rectangle = self.draw_rectangle.convert_all_rectangle_to_scale(self.drag_start_of_rectangle)
        annotation_center = screen_rectangle.center()

        # set main rotation
        annotation_rotation = self.select_current_annotation["rotation"]

        #get center local point of anotation
        local_screen_point = self.rotate_around_center_point(point_posstion, annotation_center, -annotation_rotation)

        # set new corner base no rotate no move
        new_cornerr_based = self.screen_points_to_primary_points(local_screen_point)

        # only opposite corner is stay in no move
        current_opposite_corner_map = {
            "top_left": self.drag_start_of_rectangle.bottomRight(),
            "top_right": self.drag_start_of_rectangle.bottomLeft(),
            "bottom_left": self.drag_start_of_rectangle.topRight(),
            "bottom_right": self.drag_start_of_rectangle.topLeft()
        }

        # get corner based oppsoite
        fixed_corner_based = current_opposite_corner_map[self.select_actived_hander]

        #create new rectangle from move point and stay  opposite point
        create_new_rectangle = QRectF(fixed_corner_based, new_cornerr_based).normalized()

        #save new created revtangle to current  annotation
        self.select_current_annotation["x"] = create_new_rectangle.x()
        self.select_current_annotation["y"] = create_new_rectangle.y()
        self.select_current_annotation["width"] = create_new_rectangle.width()
        self.select_current_annotation["height"] = create_new_rectangle.height()

    # drawing all hander
    def draw_selection_hander(self, current_painter, curent_frame_index):

        #if edit is not ebale or is any annotation is selected
        if not self.edit_of_annotation or self.select_current_annotation is None:
            return

        # not selected cirrent fame
        if self.select_curennt_frame_index != curent_frame_index:
            return

        # download all  rectangle
        screen_rectangle = self.get_current_annotation_rectangle(self.select_current_annotation)

        # download center of rectangle
        annotation_center = screen_rectangle.center()

        # download rotation of rectangle
        annotation_rotation = self.select_current_annotation["rotation"]

        # current paitner optinon
        current_painter.save()
        current_painter.translate(annotation_center)
        current_painter.rotate(annotation_rotation)
        current_painter.translate(-annotation_center)

        #set color and sape
        hander_pen = QPen(self.color_of_hander)
        hander_pen.setWidth(2)
        current_painter.setPen(hander_pen)
        current_painter.setBrush(QBrush(self.color_of_hander))

        # get all corners and draw them in main postion
        logical_corners = self.get_primary_corners_of_hander(screen_rectangle)
        for logical_corner in logical_corners.values():
            current_painter.drawRect(
                logical_corner.x() - self.corner_size_of_hander // 2,
                logical_corner.y() - self.corner_size_of_hander // 2,
                self.corner_size_of_hander,
                self.corner_size_of_hander
            )

        # draw rotate point
        top_center = QPoint(screen_rectangle.center().x(), screen_rectangle.top())
        rotate_handle_point = QPoint(screen_rectangle.center().x(), screen_rectangle.top() - self.rotate_offset)

        current_painter.drawLine(top_center, rotate_handle_point)
        current_painter.drawEllipse(rotate_handle_point, self.rotate_of_hander, self.rotate_of_hander)

        current_painter.restore()