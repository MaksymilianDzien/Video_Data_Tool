from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import QPoint


class Draw_polygon:

    # color of polyhon
    Color_of_polygon = QColor(155, 0, 155)

    alpha = 60

    # widget the same as rectangle , logick , and anntaion sotage
    def __init__(self, widget_image, Label_log, curennt_anotation_store):

        # set wiget, label , annotaion store
        self.widget_image = widget_image
        self.Label_log = Label_log
        self.curennt_anotation_store = curennt_anotation_store

        #self drawing mode
        #set draw
        self.set_draw_enabled = False

        #polygon numbers min
        self.target_point_count = 3

        #clicked points of polygon
        self.collected_clicked_point = []


        #mouse position of last point of polygon
        self.current_mouse_position = None


    # enable/unenable drawing with target number of points
    def draw_mod_enable(self, is_enable, point_count=3):
        #set to enable
        self.set_draw_enabled = is_enable

        #max point count or just 3
        self.target_point_count = max(point_count, 3)

        #set collection to []
        self.collected_clicked_point = []

        #set moise postion
        self.current_mouse_position = None

    #hander of mouse press - start of drawing and next clik is new polygon
    def mouse_press_handler(self, point_posstion):

        if not self.set_draw_enabled:
            return

        # current unrorate points of polygon
        point_posstion = self.widget_image.unrotate_point_of_screen(point_posstion)
        #save point to table
        self.collected_clicked_point.append(QPoint(point_posstion))


        #if it was last point then end and save poygon
        if len(self.collected_clicked_point) >= self.target_point_count:
            self.save_finish_polygon_to_anotation()
            return

        self.widget_image.update()


    #mose movnemtt  update line to next
    def mouse_move_handle(self, point_posstion):

        if not self.set_draw_enabled or not self.collected_clicked_point:
            return

        #viwe before next point is created
        point_posstion = self.widget_image.unrotate_point_of_screen(point_posstion)
        self.current_mouse_position = QPoint(point_posstion)
        self.widget_image.update()

   #
    def mouse_release_handler(self, point_posstion, curent_index_frame):
        pass

    #save finshed polygon to anntaion
    def save_finish_polygon_to_anotation(self):

        #ini fare and anntaion sotore
        anotation_store = self.curennt_anotation_store
        curent_index_frame = self.widget_image.index_frame

        #if is not in anotation_store teh set anotation_store tp []
        if curent_index_frame not in anotation_store.fream_annotation:
            anotation_store.fream_annotation[curent_index_frame] = []

        #create new polygon
        anotation_store.all_other_annotations__back(curent_index_frame)


        #conversion of each clicked point to base coordinates
        base_points = [anotation_store.convert_points_to_curent_scale(point) for point in self.collected_clicked_point]

        #ceate annotaion
        new_annotation = \
            {
                "id": anotation_store.next_annotation_id,
                "type": "polygon",
                "label_id": None,
                "rotation": 0.0,
                "layer": 1,
                #if is visible (option right panel)
                "visible": True,
                #if is locked (option right panel)
                "locked": False,
                #if is pinned (option right panel)
                "pinned": False,
                #points of polyhon
                "points": [{"x": point.x(), "y": point.y()} for point in base_points]
            }

        #add and +1 to id
        anotation_store.fream_annotation[curent_index_frame].append(new_annotation)
        anotation_store.next_annotation_id += 1

        #reset current stage for next polygon
        self.collected_clicked_point = []
        self.current_mouse_position = None

        #draw polygon
        self.widget_image.update()
        #callback right panel abaunt new annoataion
        anotation_store.current_annotations_changed()

        #create new or set laves (fuction in label_log)
        label_id, ok_input = self.Label_log.choose_annotation_label_option(self.widget_image)

        #chek if press ok_input o or is not label
        if not ok_input or label_id is None:
            # user cancelled anntaion
            anotation_store.fream_annotation[curent_index_frame].remove(new_annotation)
            self.widget_image.update()

            # delect new label if is not accepted
            anotation_store.current_annotations_changed()
            return

        #set name off addnotaion
        new_annotation["label_id"] = label_id
        self.widget_image.update()

        # call back rgitht panel ababut name label
        anotation_store.current_annotations_changed()

        # save stage to undo history
        anotation_store.on_annotion_comit()

    #drawing polygon before is created
    def draw_polygon_preview(self, polygon_painter):

        # if is not first point retun
        if not self.collected_clicked_point:
            return

        # set oval pen
        polygon_pen = QPen(self.Color_of_polygon)
        polygon_pen.setWidth(2)
        polygon_painter.setPen(polygon_pen)
        #not fill polygon yet
        polygon_painter.setBrush(QBrush(QColor(0, 0, 0, 0)))

        #drawing line bettwen points
        for index in range(len(self.collected_clicked_point) - 1):
            polygon_painter.drawLine(self.collected_clicked_point[index], self.collected_clicked_point[index + 1])

        #current moise positon (draw line before is crated)
        if self.current_mouse_position is not None:
            polygon_painter.drawLine(self.collected_clicked_point[-1], self.current_mouse_position)

        #fill all space bettwen created points
        polygon_painter.setBrush(QBrush(self.Color_of_polygon))
        for point in self.collected_clicked_point:
            polygon_painter.drawEllipse(point, 3, 3)