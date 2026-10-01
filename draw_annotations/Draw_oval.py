from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import QRect, QPoint


class Draw_oval:

    #clorlor of oval gren
    Color_of_oval = QColor(0, 170, 0)  # zielony rgb

    #Drawing Alpha
    alpha = 60

    # widget the same as rectangle , logick , and anntaion sotage
    def __init__(self, widget_image, Label_log, curennt_anotation_store):

        #set wiget, label , annotaion store
        self.widget_image = widget_image
        self.Label_log = Label_log
        self.curennt_anotation_store = curennt_anotation_store

        # self drawing mode
        #set draw
        self.set_draw_enabled = False
        #set first point
        self.mouse_first_point = None
        # init to  history to undo
        self.mouse_current_point = None

    # enable/unenable drawing
    def draw_mod_enable(self, is_enable):
        self.set_draw_enabled = is_enable

        #if oval is not complete set to
        self.mouse_first_point = None
        self.mouse_current_point = None

    # hander of mouse press - start of drawing (first point)
    def mouse_press_handler(self, point_posstion):

        if not self.set_draw_enabled:
            return

        #current unrorate points of oval
        point_posstion = self.widget_image.unrotate_point_of_screen(point_posstion)

        #set first point of oval
        self.mouse_first_point = QPoint(point_posstion)

        #set current point same as first - so preview oval can draw immediately
        self.mouse_current_point = QPoint(point_posstion)

    # drawing oval wvie
    def mouse_move_handle(self, point_posstion):

        #check if draw is enable and is set first mouse point
        if not self.set_draw_enabled or self.mouse_first_point is None:
            return

        # current unrorate points of oval
        point_posstion = self.widget_image.unrotate_point_of_screen(point_posstion)

        # ser mouse point
        self.mouse_current_point = QPoint(point_posstion)
        self.widget_image.update()

    # hander of mouse release - end of drawing
    def mouse_release_handler(self, point_posstion, curent_index_frame):

        #chek if enable
        if not self.set_draw_enabled or self.mouse_first_point is None:
            return

        #current unrorate points of oval
        point_posstion = self.widget_image.unrotate_point_of_screen(point_posstion)

        #set second point of oval
        mouse_second_point = QPoint(point_posstion)
        curent_oval = QRect(self.mouse_first_point, mouse_second_point).normalized()

        #reset points
        self.mouse_first_point = None
        self.mouse_current_point = None

        #if to small rectangle return
        if curent_oval.width() < 3 or curent_oval.height() < 3:
            self.widget_image.update()
            return

        #create new store for annotaion
        stored_oval = self.curennt_anotation_store

        #add annotation to frame
        if curent_index_frame not in stored_oval.fream_annotation:
            stored_oval.fream_annotation[curent_index_frame] = []

        #if created new annotaion all created annotaion 1 back
        stored_oval.all_other_annotations__back(curent_index_frame)

        #base oval to later getting info
        concurrent_oval = stored_oval.convert_rectangle_to_current_scale(curent_oval)

        #oval annotation info -
        new_oval_annotation = \
            {
                "id": stored_oval.next_annotation_id,
                "type": "oval",
                "label_id": None,
                #current rotaion (no connect to rotatet alll image)
                "rotation": 0.0,
                #if created new annotation is crated in first layer
                "layer": 1,
                #if is visible (option right panel)
                "visible": True,
                #if is locked (option right panel)
                "locked": False,
                "x": concurrent_oval.x(),
                "y": concurrent_oval.y(),
                "width": concurrent_oval.width(),
                "height": concurrent_oval.height()
            }

        stored_oval.fream_annotation[curent_index_frame].append(new_oval_annotation)

        #add +1 to next annotation
        stored_oval.next_annotation_id += 1

        #draw oval
        self.widget_image.update()

        #callback right panel abaunt new annoataion
        stored_oval.current_annotations_changed()

        #create new or set laves (fuction in label_log)
        label_id, ok_input = self.Label_log.choose_annotation_label_option(self.widget_image)

        #chek if press ok_input o or is not label
        if not ok_input or label_id is None:

            #user cancelled anntaion
            stored_oval.fream_annotation[curent_index_frame].remove(new_oval_annotation)
            self.widget_image.update()

            # delect new label if is not accepted
            stored_oval.current_annotations_changed()
            return

        #set name off addnotaion
        new_oval_annotation["label_id"] = label_id
        self.widget_image.update()

        #call back rgitht panel ababut name label
        stored_oval.current_annotations_changed()

        #save stage to undo history
        stored_oval.on_annotion_comit()

    #drawing annotaion before is created when is cliked
    def draw_oval_annotation(self, oval_painter):

        #if is not first point retun
        if self.mouse_first_point is None or self.mouse_current_point is None:
            return

        #set oval pen
        oval_pen = QPen(self.Color_of_oval)
        oval_pen.setWidth(2)
        oval_painter.setPen(oval_pen)

        #set fill of oval
        oval_preview_fill = QColor(self.Color_of_oval)
        oval_preview_fill.setAlpha(self.alpha)
        oval_painter.setBrush(QBrush(oval_preview_fill))

        #create oval from 2 points
        oval_preview = QRect(self.mouse_first_point, self.mouse_current_point).normalized()
        #drawing current oval from point , pen and fill
        oval_painter.drawEllipse(oval_preview)