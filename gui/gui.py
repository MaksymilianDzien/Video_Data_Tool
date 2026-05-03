from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame
)


class Main_Gui(QMainWindow):

    def __init__(self):
        super(Main_Gui, self).__init__()

        # Title and size gui
        self.setWindowTitle("Simple GUI")
        self.resize(1200, 800)
        self.Create_GUI()

    def Create_GUI(self):

        # main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # main layout
        main_gui_layout = QVBoxLayout()
        main_gui_layout.setContentsMargins(0, 0, 0, 0)
        main_gui_layout.setSpacing(0)
        main_widget.setLayout(main_gui_layout)

        # Create all panels
        main_gui_layout.addWidget(self.create_top_panel())
        main_gui_layout.addLayout(self.create_gui_main_content())
        main_gui_layout.addWidget(self.create_bottom_panel())

    # top_panel
    def create_top_panel(self):
        top_panel = QFrame()
        top_panel.setFixedHeight(60)
        top_panel.setStyleSheet("background-color: #2c3e50;")

        return top_panel

    # main_gui_layout
    def create_gui_main_content(self):
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        content_layout.addWidget(self.create_left_panel())
        content_layout.addWidget(self.create_middle_panel())
        content_layout.addWidget(self.create_right_panel())

        return content_layout

    # left_panel
    def create_left_panel(self):
        left_panel = QFrame()
        left_panel.setFixedWidth(80)
        left_panel.setStyleSheet("background-color: #e74c3c;")

        return left_panel

    # middle_panel
    def create_middle_panel(self):
        middle_panel = QFrame()
        middle_panel.setStyleSheet("background-color: #1abc9c;")

        return middle_panel

    # right_panel
    def create_right_panel(self):
        right_panel = QFrame()
        right_panel.setFixedWidth(300)
        right_panel.setStyleSheet("background-color: #f1c40f;")

        return right_panel
    # bottom_panel
    def create_bottom_panel(self):
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(80)
        bottom_bar.setStyleSheet("background-color: #244eff;")

        return bottom_bar