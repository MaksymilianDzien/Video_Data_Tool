from PyQt5 import Qt , QtCore
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout,
    QVBoxLayout, QFrame, QFileDialog, QLabel, QPushButton, QAction, QSlider,QLineEdit
)

from buttons.Button_logic_2 import ButtonLogic
from buttons.Button_logic_3 import Button3
from buttons.Button_frame_slider import Button_frame_slider

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

        # Create button layout
        top_button_layout = QHBoxLayout()
        top_button_layout.setContentsMargins(5, 5, 5, 5)
        top_button_layout.setSpacing(8)
        top_panel.setLayout(top_button_layout)

        # button style same as main window
        button_style = """
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
            """

        # top_left_button
        for i in range(1, 4):
            top_left_button = QPushButton(f"t.{i}")
            top_left_button.setFixedSize(60, 45)
            top_left_button.setStyleSheet(button_style)
            top_button_layout.addWidget(top_left_button)

        top_button_layout.addStretch()



        # frame_slider
        self.frame_slider = QSlider(QtCore.Qt.Horizontal)
        self.frame_slider.setFixedSize(250, 45)
        self.frame_slider.setMinimum(1)
        self.frame_slider.setMaximum(100)
        self.frame_slider.setValue(0)

        #frame_slider_input
        self.frame_slider_input = QLineEdit()
        self.frame_slider_input.setFixedSize(60, 45)
        self.frame_slider_input.setAlignment(QtCore.Qt.AlignCenter)
        self.frame_slider_input.setText("1")

        #add_button_slider_logick
        self.create_button_frame_slider()

        # top_mid_button
        for i in range(4, 13):
            top_mid_button = QPushButton(f"t.{i}")
            top_mid_button.setFixedSize(60, 45)
            top_mid_button.setStyleSheet(button_style)




            match i:
                #set value to start position
                case 4:
                    top_mid_button.clicked.connect(self.button_frame_slider.start_value)
                # subtract to slider value 1
                case 5:
                    top_mid_button.clicked.connect(self.button_frame_slider.down_10)
                # subtract to slider value 10
                case 6:
                    top_mid_button.clicked.connect(self.button_frame_slider.down_1)
                #add to slider value 1
                case 8:
                    top_mid_button.clicked.connect(self.button_frame_slider.up_1)
                # add to slider value 10
                case 9:
                    top_mid_button.clicked.connect(self.button_frame_slider.up_10)
                # set value to max position
                case 10:
                    top_mid_button.clicked.connect(self.button_frame_slider.max_value)

            top_button_layout.addWidget(top_mid_button)
            top_button_layout.addStretch()

            top_button_layout.addWidget(self.frame_slider)
            top_button_layout.addWidget(self.frame_slider_input)
        #input slider style
        (self.frame_slider_input.setStyleSheet
         ("""
            QLineEdit {
                background-color: #ecf0f1;
                border: 2px solid #2c3e50;
                border-radius: 6px;
                font-weight: bold;
            }
        """))

        # Slider to slider_input
        (self.frame_slider.valueChanged.connect
        (lambda slider_value: self.frame_slider_input.setText(str(slider_value)))
         )

        # slider_input to slider
        self.frame_slider_input.returnPressed.connect(self.change_slider_value)


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
            # normal mouse
            if i == 1:
                left_buttons.clicked.connect(self.disable_move_mode)
            #add moving image to second button
            if i == 2:
                 left_buttons.clicked.connect(self.enable_move_mode)
            #reset iamge positon
            #zoom button
            if i == 3:
                self.button3 = Button3(self, left_buttons)

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
        self.image = ButtonLogic()
        self.image.setText("...")


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
        for i in range(1, 8):
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
        file_path, filter = QFileDialog.getOpenFileName(self,
            "Selec image or video",
            "",
            "Media (*.png *.jpg *.jpeg *.bmp *.mp4 *.avi *.mov *.mkv)")

        if file_path:
            self.load_image_to_gui(file_path)

    #Load image
    def load_image_to_gui(self, file_path):

        #wideo format
        video_extensions = (".mp4", ".avi", ".mov", ".mkv")

        #if is wideo or image
        if file_path.lower().endswith(video_extensions):
            self.image.load_video(file_path)
        else:
            self.image.load_image(file_path)
            # reest zoom if new image is load
            self.button3.reset_zoom()

    #Add top menu
    def add_menu(self):
        menu_first_bar = self.menuBar()


        file_menu = menu_first_bar.addMenu("File")

        first_action = QAction("Find file", self)
        first_action.triggered.connect(self.find_image)

        file_menu.addAction(first_action)

    # enable mouse drag
    def enable_move_mode(self):
        self.image.enable_drag(True)
    # disable  mouse drag
    def disable_move_mode(self):
        self.image.enable_drag(False)

    #convert string to slider_value
    def change_slider_value(self):
        slider_value_text = self.frame_slider_input.text()

        #chek if value is int
        if slider_value_text.isdigit():
            slider_value = int(slider_value_text)

            if self.frame_slider.minimum() <= slider_value <= self.frame_slider.maximum():
                self.frame_slider.setValue(slider_value)
        # if is not int set value to 1
        else:
            slider_value = 1;
            self.frame_slider.setValue(slider_value)

    #button_slider_logick
    def create_button_frame_slider(self):
        self.button_frame_slider = Button_frame_slider(
            self.frame_slider,
            self.frame_slider_input
        )