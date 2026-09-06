import cv2
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QPainter, QImage
from PyQt5.QtCore import Qt, QPoint


class ButtonLogic(QLabel):

    # chabge in future ( limit bc error)
    LIMIT_VIDEO_SECONDS = 300

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

        # List of all frame (video or image)
        self.All_frames = []
        #Start value of frome index
        self.index_frame = 0

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

    # load image_images
    def load_images(self, image_paths):

        # Clear  all frames
        self.All_frames = []

        #load all images
        for image_path in image_paths:
            load_data = cv2.imread(image_path)
            if load_data is None:
                continue

            #
            processed_frame = self.process_frame(load_data)
            # add frame to list
            self.All_frames.append(self.cv_frame_to_pixmap(processed_frame))
        #set start fraome
        self.show_frame(1)

    # load video
    def load_video(self, video_path):

        #load video from path
        video = cv2.VideoCapture(video_path)

        if not video.isOpened():
            return

        # fps count
        fps = video.get(cv2.CAP_PROP_FPS)
        if not fps or fps <= 0:
            fps = 25

        # all limited frames
        limit_frames = int(fps * self.LIMIT_VIDEO_SECONDS)

        # Clear  all frames
        self.All_frames = []

        # load and chek if is in limit
        while len(self.All_frames) < limit_frames:
            ret, video_frames = video.read()

            # chek if fill is end
            if not ret:
                break

            # prossed forame
            processed_frame = self.process_frame(video_frames)
            #add frame to list
            self.All_frames.append(self.cv_frame_to_pixmap(processed_frame))
        #close video
        video.release()

        # set start fraome
        self.show_frame(1)

    # lenght of all frames
    def get_frame_count(self):
        return len(self.All_frames)

    # showing frame( connect to frame slider)
    def show_frame(self, frame_number):

        if not self.All_frames:
            return

        # conwert to table format
        index = frame_number - 1

        # IOOR
        index = max(0, min(index, len(self.All_frames) - 1))

        self.index_frame = index
        self.original_iamge = self.All_frames[index]
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

    #future add
    def process_frame(self, video_frames):
        return video_frames