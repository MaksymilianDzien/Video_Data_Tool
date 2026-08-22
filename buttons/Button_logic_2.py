import cv2
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QPainter, QImage
from PyQt5.QtCore import Qt, QPoint, QTimer


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

        self.video = None
        self.video_time = QTimer(self)
        self.video_time.timeout.connect(self.next_video_frame)



    # cv_to_pixmap
    def cv_frame_to_pixmap(self, frame):

        #create new frame
        new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_height, frame_width, frame_channel = new_frame.shape

        #add format and bytes in frame
        bytes_in_frame = frame_channel * frame_width
        q_image = (QImage(new_frame.data, frame_width, frame_height, bytes_in_frame,
        QImage.Format_RGB888))

        return QPixmap.fromImage(q_image)

    # load image/wideo
    def load_image(self, image_path):

        self.stop_video()

        load_data = cv2.imread(image_path)
        if load_data is None:
            return

        self.original_iamge = self.cv_frame_to_pixmap(load_data)
        self.update()

    # load video
    def load_video(self, video_path):


        self.stop_video()
        self.video = cv2.VideoCapture(video_path)

        if not self.video.isOpened():
            self.video_capture = None
            return

        #fps count
        fps = self.video.get(cv2.CAP_PROP_FPS)
        self.video_time.start(int(1000 / fps))

    # draw next frame
    def next_video_frame(self):

        #chek if wideo exist
        if self.video is None:
            return

        ret, video_frame = self.video.read()

        # chek if fill is end
        if not ret:
            self.stop_video()
            return

        # prossed forame
        processed_frame = self.process_frame(video_frame)

        # chane froame to pixmap
        self.original_iamge = self.cv_frame_to_pixmap(processed_frame)

        # reset QLabel
        self.update()

    # stop video if new file is read
    def stop_video(self):
        if self.video_time.isActive():
            self.video_time.stop()

        if self.video is not None:
            self.video.release()
            self.video = None

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
        if not self.drag_enabled:
            return
        if self.dragging:
            delta = event.pos() - self.last_mouse_positon
            self.positon += delta
            self.last_mouse_positon = event.pos()
            self.update()

    # mouse relase
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    #future ad d
    def process_frame(self, video_frame):
                return video_frame