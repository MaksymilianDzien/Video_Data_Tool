from PyQt5.QtCore import Qt, QPoint, QPointF, QRect
from PyQt5.QtGui import QPixmap, QKeySequence, QCursor
from PyQt5.QtWidgets import QShortcut

class Button3:

    #min zoom
    zoom_min = 0.05

    #max zoom in px
    pixels_zoom_max = 64000000

    #max side of zoom in px
    side_zoom_max = 30000

    def __init__(self, main_window, button_3):

        # main window
        self.main_window = main_window

        # button3
        self.button_3 = button_3

        # main zoom
        self.main_zoom = 1.0

        # 130%
        self.step_zoom = 1.30


        self.original_image = None

        #clicked to zoom
        self.button_3.clicked.connect(self.toggle_zoom_mode)
        self.button_3.setToolTip("Zoom: left click - zoom in 30%, right click - zoom out 30% (in the place of the cursor)")

        #zoom  - shortcut
        self.zoom_shortcut_plus = QShortcut(QKeySequence("Ctrl++"), self.main_window)
        self.zoom_shortcut_plus.activated.connect(self.zoom_in_shortcut)

        #zoom  + shortcut
        self.zoom_shortcut_minus = QShortcut(QKeySequence("Ctrl+-"), self.main_window)
        self.zoom_shortcut_minus.activated.connect(self.zoom_out_shortcut)

    #enable zoom mode
    def toggle_zoom_mode(self):

        #if is enabled then disable
        if self.main_window.image.zoom_enabled:
            self.main_window.disable_move_mode()
            return

        #set window
        main_window = self.main_window

        #disable other
        main_window.image.enable_drag(False)
        main_window.image.enable_edit_mode(False)

        main_window.draw_mode_enabled = False
        main_window.image.enable_draw_mode(False)

        main_window.draw_oval_mode_enabled = False
        main_window.image.enable_oval_draw_mode(False)

        main_window.button_polygon_option.polygon_option_deactivate()
        main_window.button_magic_wand.magic_wand_deactivate()

        main_window.image.enable_zoom_mode(True)

    #disable mode
    def zoom_deactivate(self):
        self.main_window.image.enable_zoom_mode(False)

    #clicked in image
    def mouse_press_handler(self, point_of_screen, mouse_button):

        #left
        if mouse_button == Qt.LeftButton:
            self.zoom_image(point_of_screen, self.step_zoom)

        #right
        elif mouse_button == Qt.RightButton:
            self.zoom_image(point_of_screen, 1 / self.step_zoom)

    # chek if mouse  is clicked in image
    def point_is_inside_frame(self, point_of_screen):

        zoom_image = self.main_window.image

        if zoom_image.original_iamge is None:
            return False

        #point before rotation
        point_without_rotation = zoom_image.unrotate_point_of_screen(point_of_screen)

        #prime frame rect
        prime_frame_rect = QRect(zoom_image.positon, zoom_image.original_iamge.size())

        return prime_frame_rect.contains(point_without_rotation)

    #zoom where mouse cursor
    def zoom_image(self, point_of_screen, zoom_factor):

        #
        zoom_image = self.main_window.image

        if zoom_image.original_iamge is None:
            return

        #if not in frame
        if not self.point_is_inside_frame(point_of_screen):
            return

        # orginal image
        if self.original_image is None:

            self.original_image = (QPixmap(zoom_image.original_iamge))

        #set new zoom
        new_zoom = self.main_zoom * zoom_factor

        #set  width and height for  new image
        width = (int(self.original_image.width() * new_zoom))

        height = (int(self.original_image.height() * new_zoom))

        #limits of zoom
        if zoom_factor < 1 and (new_zoom < self.zoom_min or width < 1 or height < 1):
            return
        if zoom_factor > 1 and (width * height > self.pixels_zoom_max or max(width, height) > self.side_zoom_max):
            return

        #old center of image
        old_center_iamge = QPointF(
            zoom_image.positon.x() + zoom_image.original_iamge.width() / 2,
            zoom_image.positon.y() + zoom_image.original_iamge.height() / 2)

        # create new bigger iamge
        scaled_image = self.original_image.scaled(
            width,
            height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation)

        #new center of image
        zoom_ratio = new_zoom / self.main_zoom
        cursor_point = QPointF(point_of_screen)
        new_center_iamge = cursor_point + (old_center_iamge - cursor_point) * zoom_ratio

        #new position of
        zoom_image.positon = QPoint(
            round(new_center_iamge.x() - scaled_image.width() / 2),
            round(new_center_iamge.y() - scaled_image.height() / 2))

        # zoom
        self.main_zoom = new_zoom

        # set zoom to scale labes darwing
        zoom_image.base_zoom_level = self.main_zoom

        # connect new image
        #  ButtonLogic
        zoom_image.original_iamge = scaled_image

        # update
        zoom_image.update()

    def reset_zoom(self):
        #reset zoom
        self.main_zoom = 1.0
        self.original_image = None

        #reset zoom to curret value
        self.main_window.image.base_zoom_level = 1.0

    #shortcut zoom in
    def zoom_in_shortcut(self):
        cursor_point = self.main_window.image.mapFromGlobal(QCursor.pos())

        #if cursor is not in frame
        if not self.main_window.image.rect().contains(cursor_point):
            return

        self.zoom_image(cursor_point, self.step_zoom)

    # shortcut zoom out
    def zoom_out_shortcut(self):
        cursor_point = self.main_window.image.mapFromGlobal(QCursor.pos())

        # if cursor is not in frame
        if not self.main_window.image.rect().contains(cursor_point):
            return

        self.zoom_image(cursor_point, 1 / self.step_zoom)