from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QPoint


class ButtonLogic(QLabel):

    def __init__(self):
        super().__init__()
        # center image
        self.setAlignment(Qt.AlignCenter)

        self.original_iamge = None

        # image positon
        self.positon = QPoint(0, 0)

        # drags flags
        self.drag_enabled = False
        self.dragging = False

        self.last_mouse_positon = QPoint()

    # load image
    def load_image(self, image_path):
        image = QPixmap(image_path)

        self.original_iamge = image
        self.update()

    #  enable/unenable drag
    def enable_drag(self, enabled):
        self.drag_enabled = enabled

    # paint image
    def paintEvent(self, event):

        super().paintEvent(event)

        if not self.original_iamge:
            return

        iamge_painter = QPainter(self)

        x_positon = self.positon.x()
        y_positon = self.positon.y()

        iamge_painter.drawPixmap(x_positon, y_positon, self.original_iamge)

    # mose Event
    def mousePressEvent(self, event):

        if self.drag_enabled and event.button() == Qt.LeftButton:
            self.dragging = True
            self.last_mouse_positon = event.pos()

    # Mouse move
    def mouseMoveEvent(self, event):

        if self.dragging:

            delta = event.pos() - self.last_mouse_positon
            self.positon += delta
            self.last_mouse_positon = event.pos()
            self.update()

    # mouse relase
    def mouseReleaseEvent(self, event):

        self.dragging = False