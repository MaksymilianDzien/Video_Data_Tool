from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class Button3:

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
        self.button_3.clicked.connect(self.zoom_image)

    def zoom_image(self):

        #
        zoom_image = self.main_window.image

        if zoom_image.original_iamge is None:
            return

        # orginal image
        if self.original_image is None:

            self.original_image = QPixmap(
                zoom_image.original_iamge
            )

        # zoom + 30 %
        self.main_zoom *= self.step_zoom

        # calculeate new image
        width = int(
            self.original_image.width() * self.main_zoom
        )


        height = int(
            self.original_image.height() * self.main_zoom
        )

        # create new bigger iamge
        scaled_image = self.original_image.scaled(
            width,
            height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        # connect new image
        #  ButtonLogic
        zoom_image.original_iamge = scaled_image

        # update
        zoom_image.update()

    def reset_zoom(self):
        #reset zoom
        self.main_zoom = 1.0
        self.original_image = None