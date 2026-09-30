import math
from PyQt5.QtGui import QPen, QBrush, QColor, QPolygonF
from PyQt5.QtCore import QPoint, QPointF, QRectF, Qt


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

        #copy of start polygon points
        self.polygon_drag_points = None

        #set  draging all annotaion
        self.drag_annotaion_mouse_start = None

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
        self.polygon_drag_points = None
        self.drag_annotaion_mouse_start = None

    # rectangle after calkulated zomm and rotate
    def get_current_annotation_rectangle(self, annotation):

        #if type is polygon
        if annotation.get("type") == "polygon":
            base_polygon = self.draw_rectangle.build_polygon_for_annotation_info(annotation)
            base_rectangle = base_polygon.boundingRect()
        else:
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

        #new type of handler if is polygon
        if self.select_current_annotation.get("type") == "polygon":
            return self.find_polygon_hander_press(point_posstion, self.select_current_annotation)

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

    #polygon hander
    def find_polygon_hander_press(self, point_posstion, annotation):

        #download all  polygon
        screen_rectangle = self.get_current_annotation_rectangle(annotation)
        #download center of polygon
        annotation_center = screen_rectangle.center()
        #download rotation of polygon
        annotation_rotation = annotation["rotation"]

        #main rotate hander not rotated
        logical_rotate_hander = QPoint(screen_rectangle.center().x(), screen_rectangle.top() - self.rotate_offset)
        #rotate hander after
        visual_rotate_hander = self.rotate_around_center_point(logical_rotate_hander, annotation_center, annotation_rotation)

        #sqr(dx^2 + dy^2)
        distance_rotated_hander = math.hypot(
            point_posstion.x() - visual_rotate_hander.x(),
            point_posstion.y() - visual_rotate_hander.y()
        )

        #if is too small
        if distance_rotated_hander <= self.rotate_of_hander + 4:
            return "rotate"

        #hander in all  polygon points
        base_polygon = self.draw_rectangle.build_polygon_for_annotation_info(annotation)

        #connect all points
        for index, base_point in enumerate(base_polygon):
            screen_point = self.draw_rectangle.convert_points_to_scren_scale(base_point)
            visual_point = self.rotate_around_center_point(screen_point, annotation_center, annotation_rotation)

            #check abs of posstion
            if abs(point_posstion.x() - visual_point.x()) <= self.corner_size_of_hander \
                    and abs(point_posstion.y() - visual_point.y()) <= self.corner_size_of_hander:
                return f"vertex:{index}"

        return None

    # chek if point is in anotation
    def is_point_in_rotated_anotation(self, point_posstion, annotation):

        # download center of rectangle
        screen_rectangle = self.get_current_annotation_rectangle(annotation)

        # download rotation of rectangle
        annotation_center = screen_rectangle.center()

        # get center local point of anotation
        local_point = self.rotate_around_center_point(point_posstion, annotation_center, -annotation["rotation"])

        current_annotation_type = annotation.get("type")

        #check if is oval type retrun is point in eclpsce
        if current_annotation_type == "oval":
            return self.points_in_ellipse(local_point, screen_rectangle)

        #chcek if point is in fill of polygon
        if current_annotation_type == "polygon":
            base_polygon = self.draw_rectangle.build_polygon_for_annotation_info(annotation)
            screen_polygon = QPolygonF([
                QPointF(self.draw_rectangle.convert_points_to_scren_scale(point)) for point in base_polygon
            ])
            return screen_polygon.containsPoint(QPointF(local_point), Qt.OddEvenFill)

        return screen_rectangle.contains(local_point)


    #check if point is in ellpise
    def points_in_ellipse(self, local_point, screen_rectangle):

        #value of center / x and y radus of ellipse
        center_of_ellipse = screen_rectangle.center()
        x_radius_of_ellipse = screen_rectangle.width() / 2
        y_radius_of_ellipse = screen_rectangle.height() / 2

        #if x or y is negative then return false
        if x_radius_of_ellipse <= 0 or y_radius_of_ellipse <= 0:
            return False

        #cal of ellipse  ( (x-cx) / rx )^2 + ( (y-cy) / ry)^2
        x_normalize_ellipse = (local_point.x() - center_of_ellipse.x()) / x_radius_of_ellipse
        y_normalize_ellipse = (local_point.y() - center_of_ellipse.y()) / y_radius_of_ellipse

        return (x_normalize_ellipse ** 2 + y_normalize_ellipse ** 2) <= 1


    def mouse_press_hander(self, point_posstion, curent_index_frame):

        # if eidt is not enable
        if not self.edit_of_annotation:
            return

        # current unrorate points of rectangle
        point_posstion = self.current_widget_image.unrotate_point_of_screen(point_posstion)

        # chek if hander is selected
        if self.select_current_annotation is not None and self.select_curennt_frame_index == curent_index_frame:

            #save current hander preset
            handle_name = self.find_hander_press(point_posstion)

            if handle_name is not None:

                # what hander is actived
                self.select_actived_hander = handle_name

                #if is polygon save pints else just drag start retagle
                if self.select_current_annotation.get("type") == "polygon":
                    self.polygon_drag_points = [dict(point) for point in self.select_current_annotation["points"]]
                    self.drag_start_of_rectangle = None
                else:
                    self.drag_start_of_rectangle = self.draw_rectangle.build_rectangle_for_annotation_info(self.select_current_annotation)
                    self.polygon_drag_points = None
                return


        # if hander is not clicked then chek if clicked in annotation itself (sorted layer)
        frame_annotations = self.draw_rectangle.get_annotations_for_click(curent_index_frame)

        for annotation in frame_annotations:
            if self.is_point_in_rotated_anotation(point_posstion, annotation):
                # if is cliked get this annotation in front first layer
                self.draw_rectangle.annotations_to_front(curent_index_frame, annotation)

                self.select_current_annotation = annotation
                self.select_curennt_frame_index = curent_index_frame

                # if annotaion is cliked in annotaion then set to move all annotaion
                self.select_actived_hander = "move"

                #save list of points if is polygon else  bounding rect
                if annotation.get("type") == "polygon":
                    self.polygon_drag_points = [dict(point) for point in annotation["points"]]
                    self.drag_start_of_rectangle = None
                else:
                    self.drag_start_of_rectangle = self.draw_rectangle.build_rectangle_for_annotation_info(annotation)
                    self.polygon_drag_points = None

                # current mosue position
                self.drag_annotaion_mouse_start = QPoint(point_posstion)
                # redraw change annotaion
                self.current_widget_image.update()
                return

        # miss or not select any annotations disable edit annotations and update current image
        self.deselecte_edited_mode()
        self.current_widget_image.update()

    def mouse_move_hander(self, point_posstion):

        # if is not enable or is not selectet or is not active
        if not self.edit_of_annotation or self.select_actived_hander is None or self.select_current_annotation is None:
            return

        # current unrorate points of rectangle
        point_posstion = self.current_widget_image.unrotate_point_of_screen(point_posstion)

        #if rotate hander is selected
        if self.select_actived_hander == "rotate":
            self.update_annotation_rotation(point_posstion)
        # if move  then move all annotaion with mouse
        elif self.select_actived_hander == "move":
            self.move_current_selected_annotation(point_posstion)
        # if point of polygon is moving
        elif isinstance(self.select_actived_hander, str) and self.select_actived_hander.startswith("vertex:"):
            self.update_polygon_hander(point_posstion)
        # if any else hander is selected (rog prostokata/owalu)
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
        self.polygon_drag_points = None
        self.drag_annotaion_mouse_start = None

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

    #change annotaion witch pressed mosue in annotaion
    def move_current_selected_annotation(self, point_posstion):

        current_zoom_level = self.current_widget_image.base_zoom_level

        # delta points
        delta_x = point_posstion.x() - self.drag_annotaion_mouse_start.x()
        delta_y = point_posstion.y() - self.drag_annotaion_mouse_start.y()

        # delta points without zoom
        true_delta_x = delta_x / current_zoom_level
        true_delta_y = delta_y / current_zoom_level

        #polygon move all points
        if self.select_current_annotation.get("type") == "polygon":
            self.select_current_annotation["points"] = [
                {"x": point["x"] + true_delta_x, "y": point["y"] + true_delta_y}
                for point in self.polygon_drag_points
            ]
            return

        #created new rectangle with move points
        new_moved_rectangle = self.drag_start_of_rectangle.translated(true_delta_x, true_delta_y)

        #set new created rectangle witch new points
        self.select_current_annotation["x"] = new_moved_rectangle.x()
        self.select_current_annotation["y"] = new_moved_rectangle.y()
        self.select_current_annotation["width"] = new_moved_rectangle.width()
        self.select_current_annotation["height"] = new_moved_rectangle.height()

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

    #move only one hander of polygon
    def update_polygon_hander(self, point_posstion):

        #vertex index
        current_vertex_index = int(self.select_actived_hander.split(":")[1])

        #copy of all points of polygon
        base_polygon_start = [QPointF(point["x"], point["y"]) for point in self.polygon_drag_points]
        #base point of polygon
        screen_polygon_start = QPolygonF([
            QPointF(self.draw_rectangle.convert_points_to_scren_scale(point)) for point in base_polygon_start
        ])
        #center of anntaion
        annotation_center = screen_polygon_start.boundingRect().center()

        #angle of anntaion
        annotation_rotation = self.select_current_annotation["rotation"]

        #center and point positaion -rotaion and center
        local_screen_point = self.rotate_around_center_point(point_posstion, annotation_center, -annotation_rotation)
        #new base point of polygon
        new_point_base = self.screen_points_to_primary_points(local_screen_point)

        #coppy list of polygon drag points
        updated_points = [dict(point) for point in self.polygon_drag_points]
        #update one point of this list
        updated_points[current_vertex_index] = {"x": new_point_base.x(), "y": new_point_base.y()}

        #save list with new updated points
        self.select_current_annotation["points"] = updated_points

    # drawing all hander
    def draw_selection_hander(self, current_painter, curent_frame_index):

        #if edit is not ebale or is any annotation is selected
        if not self.edit_of_annotation or self.select_current_annotation is None:
            return

        # not selected cirrent fame
        if self.select_curennt_frame_index != curent_frame_index:
            return

        #no draw hander if is not visable
        if not self.select_current_annotation.get("visible", True):
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

        #polygon all points are hander
        if self.select_current_annotation.get("type") == "polygon":
            base_polygon = self.draw_rectangle.build_polygon_for_annotation_info(self.select_current_annotation)
            for base_point in base_polygon:
                screen_point = self.draw_rectangle.convert_points_to_scren_scale(base_point)
                current_painter.drawRect(
                    screen_point.x() - self.corner_size_of_hander // 2,
                    screen_point.y() - self.corner_size_of_hander // 2,
                    self.corner_size_of_hander,
                    self.corner_size_of_hander
                )
        else:
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