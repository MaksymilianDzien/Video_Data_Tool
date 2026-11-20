import re
from PyQt5.QtCore import QObject, QEvent, QTimer


class Drag_drop_files(QObject):

    #iamge file extensions
    image_extensions = (".png", ".jpg", ".jpeg", ".bmp")

    #video file extensions
    video_extensions = (".mp4", ".avi", ".mov", ".mkv")

    def __init__(self, current_main_window, drop_panel):
        super().__init__()

        #set  main widow
        self.main_window = current_main_window

        #set mid panel for get file in window
        self.dropped_panel = drop_panel
        self.dropped_panel.setAcceptDrops(True)
        self.dropped_panel.installEventFilter(self)

        #accept dropped files
        self.dropped_image = current_main_window.image
        self.dropped_image.setAcceptDrops(True)
        self.dropped_image.installEventFilter(self)

        #set list of path for drop file
        self.dropped_paths = []

    #get paths of drop files
    def get_dropped_paths_for_files(self, mime_data):

        #chek if is file
        if not mime_data.hasUrls():
            return []

        #all path image or video other file not load
        dropped_image_paths = []
        dropped_video_paths = []
        for dropped_url in mime_data.urls():

            #path for file
            dropped_path = dropped_url.toLocalFile()

            #only images
            if dropped_path.lower().endswith(self.image_extensions):
                dropped_image_paths.append(dropped_path)

            #wideo
            elif dropped_path.lower().endswith(self.video_extensions):
                dropped_video_paths.append(dropped_path)

        #only one video
        if dropped_video_paths:
            if len(dropped_video_paths) == 1 and not dropped_image_paths:
                return dropped_video_paths
            return []

        #sort in name file
        dropped_image_paths.sort(key=self.natural_sort_key)

        return dropped_image_paths

    #sorted compared as numbers
    def natural_sort_key(self, path_of_file):

        #separation into text and numbers
        parts_of_path = re.split(r"(\d+)", path_of_file.lower())

        return [int(part) if index % 2 else part for index, part in enumerate(parts_of_path)]

    #event for drag and drop btw image and panel
    def eventFilter(self, watched_object, current_event):

        #set event
        event_type = current_event.type()


        #drag in panel check if is  file extensions
        if event_type in (QEvent.DragEnter, QEvent.DragMove):
            if self.get_dropped_paths_for_files(current_event.mimeData()):
                current_event.acceptProposedAction()
            else:
                current_event.ignore()
            return True

        #drop file in panel
        if event_type == QEvent.Drop:
            self.dropped_paths = self.get_dropped_paths_for_files(current_event.mimeData())

            if self.dropped_paths:
                current_event.acceptProposedAction()

                #load file after drag
                QTimer.singleShot(0, self.load_dropped_files)
            else:
                current_event.ignore()
            return True


        return False


    #load drop files
    def load_dropped_files(self):

        paths_to_load = self.dropped_paths
        self.dropped_paths = []

        if not paths_to_load:
            return

        self.main_window.load_image_to_gui(paths_to_load)