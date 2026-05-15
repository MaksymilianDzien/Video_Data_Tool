from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QFileDialog, QLabel, QPushButton, QAction
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class Main_Gui(QMainWindow):

    def __init__(self):
        super(Main_Gui, self).__init__()

        # Title and size gui
        self.setWindowTitle("Simple GUI")
        self.resize(1200, 800)
        self.Create_GUI()
        self.add_menu()

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
        #Create button
        button_layout = QHBoxLayout()
        top_panel.setLayout(button_layout)

        button_layout.addStretch()

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

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(5, 5, 5, 5)
        left_layout.setSpacing(8)

        # Create 7 buttons
        for i in range(1, 9):
            left_buttons = QPushButton(str(i))


            # size
            left_buttons.setFixedSize(60, 60)

            # style of button
            left_buttons.setStyleSheet("""
                QPushButton {
                    background-color: #ecf0f1;
                    border: 2px solid #2c3e50;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #bdc3c7;
                }
                QPushButton:pressed {
                    background-color: #95a5a6;
                }
            """)

            left_layout.addWidget(left_buttons)

        left_layout.addStretch()
        left_panel.setLayout(left_layout)
        return left_panel

    # middle_panel
    def create_middle_panel(self):
        middle_panel = QFrame()
        middle_panel.setStyleSheet("background-color: #1abc9c;")

        image_layout = QVBoxLayout()
        middle_panel.setLayout(image_layout)
        #Add image to layout
        self.image = QLabel("...")
        self.image.setAlignment(Qt.AlignCenter)

        image_layout.addWidget(self.image)

        return middle_panel

    # right_panel
    def create_right_panel(self):
        right_panel = QFrame()
        right_panel.setFixedWidth(300)
        right_panel.setStyleSheet("background-color: #f1c40f;")

        return right_panel

    # bottom_panel
    def create_bottom_panel(self):
        bottom_panel = QFrame()
        bottom_panel.setFixedHeight(80)
        bottom_panel.setStyleSheet("background-color: #244eff;")
        # layout
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(10, 10, 10, 10)
        bottom_layout.setSpacing(10)

        # center button
        bottom_layout.addStretch()

        # Create 3 buttons
        for i in range(1, 4):
            bottom_buttons = QPushButton(str(i))

            # size
            bottom_buttons.setFixedSize(60, 60)

            # style of button
            bottom_buttons.setStyleSheet("""
                QPushButton {
                    background-color: #ecf0f1;
                    border: 2px solid #2c3e50;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #bdc3c7;
                }
                QPushButton:pressed {
                    background-color: #95a5a6;
                }
            """)

            bottom_layout.addWidget(bottom_buttons)

        bottom_layout.addStretch()

        bottom_panel.setLayout(bottom_layout)

        return bottom_panel

    #Find file
    def find_image(self):
        image_path, filter = QFileDialog.getOpenFileName(self,"Selec image","","Images (*.png *.jpg *.jpeg *.bmp)")

        if image_path:
            self.load_image_to_gui(image_path)
    #Load image
    def load_image_to_gui(self,image_path):
        load_image = QPixmap(image_path)

        self.image.setPixmap(load_image.scaled(self.image.size(), Qt.KeepAspectRatio))

    #Add top menu
    def add_menu(self):
        menu_first_bar = self.menuBar()

        file_menu = menu_first_bar.addMenu("File")

        first_action = QAction("Find file", self)
        first_action.triggered.connect(self.find_image)

        file_menu.addAction(first_action)