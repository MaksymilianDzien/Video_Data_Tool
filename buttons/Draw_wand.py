import math
import cv2
import numpy as np
from PyQt5.QtGui import QPen, QBrush, QColor, QImage, QPolygon, QKeySequence
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtWidgets import QShortcut


#select and drawing  polygon
class Draw_wand:

    #color of wand
    Color_of_wand = QColor(0, 160, 255)

    #alpha
    alpha = 60

    #polygon simplification
    simplify_percent = 0.006

    #minimum simplification in pixels
    min_simplify_pixels = 2.0

    #minimum selection area in pixels
    min_area_pixels = 20


    def __init__(self, widget_image, Label_log, curennt_anotation_store):

        #remember widget, log label, and annotation store
        self.widget_image = widget_image
        self.Label_log = Label_log
        self.curennt_anotation_store = curennt_anotation_store

        #set draw enable
        self.set_draw_enabled = False

        #tolerance of color
        self.tolerance = 20

        #current frame as a NumPy array
        self.frame_for_wand = None

        # frame key
        self.frame_key = None

        #selected area (0/255 mask)
        self.selected_mask = None
        self.selected_key = None

        #ponts of polygon
        self.preview_points = []

        # all shorcut
        self.magic_wand_all_shortcut()

        #fill mask
        self.fill_mask = None

    #enable / disable wand
    def draw_mod_enable(self, is_enable, tolerance=20):

        self.set_draw_enabled = is_enable

        #tolerance btw 0 and 100
        self.tolerance = max(0, min(int(tolerance), 100))

        #clear old selection
        self.clear_selection()

        #shortcut work only if is enable
        self.set_shortcut_enabled(is_enable)

        self.widget_image.update()

    #clear selection and mask
    def clear_selection(self):
        self.selected_mask = None
        self.selected_key = None
        self.preview_points = []

    #current frame key
    def get_current_frame_key(self):

        frames = self.widget_image.All_frames
        frame_index = self.widget_image.index_frame

        if not frames or frame_index >= len(frames):
            return None

        return (frame_index, frames[frame_index].cacheKey())

    #convert pixmap to nupy
    def convert_pixmap_to_numpy(self, pixmap):

        # RGB32 = 4 B/px, bytesPerLine == width * 4
        q_image = pixmap.toImage().convertToFormat(QImage.Format_RGB32)
        width = q_image.width()
        height = q_image.height()

        pointer = q_image.constBits()
        pointer.setsize(height * width * 4)

        #view of a QImage buffer, without copying
        bgra = np.frombuffer(pointer, dtype=np.uint8).reshape(height, width, 4)

        # one copy
        return cv2.cvtColor(bgra, cv2.COLOR_BGRA2RGB)

    #get the current frame as a numpy array
    def get_frame_for_wand(self):

        current_key = self.get_current_frame_key()
        if current_key is None:
            return None

        if current_key != self.frame_key:
            #clear old frame
            self.frame_for_wand = None
            self.fill_mask = None
            self.frame_key = None

            frame = self.convert_pixmap_to_numpy(self.widget_image.All_frames[current_key[0]])
            # median filter removes noise
            self.frame_for_wand = cv2.medianBlur(frame, 3)
            del frame

            self.frame_key = current_key

        return self.frame_for_wand

    #area similar color around the clicked pixel
    def get_region_of_click(self, frame, pixel_x, pixel_y):

        height, width = frame.shape[:2]

        if self.fill_mask is None or self.fill_mask.shape != (height + 2, width + 2):
            self.fill_mask = np.zeros((height + 2, width + 2), dtype=np.uint8)
        else:
            self.fill_mask.fill(0)

        tolerance_of_color = (self.tolerance, self.tolerance, self.tolerance)

        flags = 4 | cv2.FLOODFILL_MASK_ONLY | cv2.FLOODFILL_FIXED_RANGE | (255 << 8)
        cv2.floodFill(frame, self.fill_mask, (pixel_x, pixel_y), 0, tolerance_of_color, tolerance_of_color, flags)

        # view of the shared mask,
        return self.fill_mask[1:-1, 1:-1]

    #largest mask outline as a simplified polygon
    def get_polygon_points_of_mask(self, mask):


        #only contours
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        if not contours:
            return []

        #select biggest contours
        biggest_contour = max(contours, key=cv2.contourArea)

        if cv2.contourArea(biggest_contour) < self.min_area_pixels:
            return []

        #fewer points is easier to edit polygon
        perimeter = cv2.arcLength(biggest_contour, True)
        epsilon = max(self.min_simplify_pixels, self.simplify_percent * perimeter)
        simplified_contour = cv2.approxPolyDP(biggest_contour, epsilon, True)

        if len(simplified_contour) < 3:
            return []


        return [(float(point[0][0]) + 0.5, float(point[0][1]) + 0.5) for point in simplified_contour]

    #klik myszy: lewy dodaje obszar, prawy odejmuje obszar
    def mouse_press_handler(self, point_posstion, mouse_button):

        if not self.set_draw_enabled:
            return

        frame = self.get_frame_for_wand()
        if frame is None:
            return

        #clicked point converted to base coordinates
        point_posstion = self.widget_image.unrotate_point_of_screen(point_posstion)
        base_point = self.curennt_anotation_store.convert_points_to_curent_scale(point_posstion)

        pixel_x = int(math.floor(base_point.x()))
        pixel_y = int(math.floor(base_point.y()))

        height, width = frame.shape[:2]

        #clicking outside the image does nothing
        if pixel_x < 0 or pixel_y < 0 or pixel_x >= width or pixel_y >= height:
            return

        #the selection from another frame no longer fits – start over
        if self.selected_key != self.frame_key or self.selected_mask is None:
            self.selected_mask = np.zeros((height, width), dtype=np.uint8)
            self.selected_key = self.frame_key

        clicked_region = self.get_region_of_click(frame, pixel_x, pixel_y)

        if mouse_button == Qt.RightButton:
            #add mask
            self.selected_mask[clicked_region > 0] = 0
        else:
            #delete mask
            self.selected_mask[clicked_region > 0] = 255

        self.preview_points = self.get_polygon_points_of_mask(self.selected_mask)

        self.widget_image.update()

    #drawing polygon
    def draw_magic_wand_preview(self, wand_painter):

        if not self.set_draw_enabled or not self.preview_points:
            return

        #the selection from another frame no longer fits – start over
        if self.selected_key != self.get_current_frame_key():
            return

        #base points to screen points
        screen_points = [
            self.curennt_anotation_store.convert_points_to_scren_scale(QPointF(point_x, point_y))
            for point_x, point_y in self.preview_points]

        wand_pen = QPen(self.Color_of_wand)
        wand_pen.setWidth(2)
        wand_painter.setPen(wand_pen)

        #polygon fill
        wand_painter.setBrush(QBrush(QColor(
            self.Color_of_wand.red(), self.Color_of_wand.green(), self.Color_of_wand.blue(), self.alpha
        )))
        wand_painter.drawPolygon(QPolygon(screen_points))

        #polygon points
        wand_painter.setBrush(QBrush(self.Color_of_wand))
        for point in screen_points:
            wand_painter.drawEllipse(point, 3, 3)

    #save polygon as anotation(Enter)
    def finish_magic_wand_polygon(self):

        if not self.set_draw_enabled:
            return

        #not selected or not in frame return
        if len(self.preview_points) < 3 or self.selected_key != self.get_current_frame_key():
            return

        #annotation store and frame number
        anotation_store = self.curennt_anotation_store
        curent_index_frame = self.widget_image.index_frame

        #if frame don't have list of anotation create one
        if curent_index_frame not in anotation_store.fream_annotation:
            anotation_store.fream_annotation[curent_index_frame] = []

        #all other  annotations back
        anotation_store.all_other_annotations__back(curent_index_frame)

        #new annotation
        new_annotation = \
            {
                "id": anotation_store.next_annotation_id,
                "type": "polygon",
                "label_id": None,
                "rotation": 0.0,
                "layer": 1,
                "visible": True,
                "locked": False,
                "pinned": False,
                "points": [{"x": point_x, "y": point_y} for point_x, point_y in self.preview_points]
            }

        #add an annotation and increment the ID by 1
        anotation_store.fream_annotation[curent_index_frame].append(new_annotation)
        anotation_store.next_annotation_id += 1

        #update image and right panel
        self.widget_image.update()
        anotation_store.current_annotations_changed()

        #select or create label
        label_id, ok_input = self.Label_log.choose_annotation_label_option(self.widget_image)

        #user cancelled label selection
        if not ok_input or label_id is None:
            #usun adnotacje, zaznaczenie rozdzki zostaje (mozna sprobowac jeszcze raz)
            #delete  anotation
            anotation_store.fream_annotation[curent_index_frame].remove(new_annotation)
            self.widget_image.update()
            anotation_store.current_annotations_changed()
            return

        #set anotation label
        new_annotation["label_id"] = label_id

        #enable  disable edit mode
        self.widget_image.window().disable_move_mode()

        #new anotation is edit mode
        self.widget_image.edit_current_anotation.select_annotation_right_panel(new_annotation, curent_index_frame)
        self.widget_image.update()

        #update right panel
        anotation_store.current_annotations_changed()

        #add to ctrl + z history
        anotation_store.on_annotion_comit()

    #cancel current magic wand selection (Esc)
    def cancel_magic_wand_selection(self):

        if not self.set_draw_enabled:
            return

        self.clear_selection()
        self.widget_image.update()

    #enable shortcut
    def set_shortcut_enabled(self, is_enable):
        self.shortcut_finish_return.setEnabled(is_enable)
        self.shortcut_cancel.setEnabled(is_enable)

    #all shortcut
    def magic_wand_all_shortcut(self):

        #Enter - save
        self.shortcut_finish_return = QShortcut(QKeySequence("Return"), self.widget_image)
        self.shortcut_finish_return.activated.connect(self.finish_magic_wand_polygon)

        #Esc - cancel
        self.shortcut_cancel = QShortcut(QKeySequence("Esc"), self.widget_image)
        self.shortcut_cancel.activated.connect(self.cancel_magic_wand_selection)

        #at the start, the wand is disabled
        self.set_shortcut_enabled(False)