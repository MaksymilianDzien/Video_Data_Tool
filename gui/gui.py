from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame
)

class Main_Gui(QMainWindow):
    def __init__(self):
        super().__init__()

        # Title and size gui
        self.setWindowTitle("Simpe GUI")
        self.resize(1200, 800)

        # main widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # top_panel
        self.top_panel = QFrame()
        self.top_panel.setFixedHeight(60)
        self.top_panel.setStyleSheet("background-color: #2c3e50;")
        main_layout.addWidget(self.top_panel)

        # main_gui_layout
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # left_panel
        self.left_panel = QFrame()
        self.left_panel.setFixedWidth(80)
        self.left_panel.setStyleSheet("background-color: #e74c3c;")
        content_layout.addWidget(self.left_panel)

        # middle_panel
        self.middle_panel = QFrame()
        self.middle_panel.setStyleSheet("background-color: #1abc9c;")
        content_layout.addWidget(self.middle_panel)

        # right_panel
        self.right_panel = QFrame()
        self.right_panel.setFixedWidth(300)
        self.right_panel.setStyleSheet("background-color: #f1c40f;")
        content_layout.addWidget(self.right_panel)