from PyQt5 import Qt , QtCore
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout,
    QVBoxLayout, QFrame, QFileDialog, QLabel, QPushButton, QAction, QSlider,QLineEdit, QMessageBox
)
from buttons.Button_polygon_option import Button_polygon_option
from buttons.Button_rotated_option import Button_rotated_option
from buttons.Button_ctrl_z import Button_ctrl_z
from buttons.Button_logic_2 import ButtonLogic
from buttons.Button_logic_3 import Button3
from buttons.Button_frame_slider import Button_frame_slider
from draw_annotations.Main_Right_Panel_Label_Info import  Main_Right_Panel_Label_Info
import os
from PyQt5.QtGui import QIcon
from core.Saved_project import Saved_project

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

        #first create booton panel before mid panel
        bottom_panel = self.create_bottom_panel()

        # Create all panels
        main_gui_layout.addWidget(self.create_top_panel())
        main_gui_layout.addLayout(self.create_gui_main_content())
        main_gui_layout.addWidget(bottom_panel)

    #create top panel
    def create_top_panel(self):
        top_panel = QFrame()
        top_panel.setFixedHeight(80)
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

            # t.2 - ctl + z
            if i == 2:
                self.button_ctrl_z = Button_ctrl_z(self, top_left_button)

            top_button_layout.addWidget(top_left_button)

        top_button_layout.addStretch()

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
        left_panel.setFixedWidth(50)
        left_panel.setStyleSheet("background-color: #e74c3c;")

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(5, 5, 5, 5)
        left_layout.setSpacing(4)

        # set drawing value
        self.draw_mode_enabled = False
        self.draw_oval_mode_enabled = False

        # folder with left_panel_icons
        left_panel_icon_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "left_panel_icons"
        )

        # left_panel_icons for buttons
        left_panel_icon_paths = {
            1: os.path.join(left_panel_icon_folder, "mouse.png"),
            2: os.path.join(left_panel_icon_folder, "move.png"),
            3: os.path.join(left_panel_icon_folder, "zoom.png"),
            4: os.path.join(left_panel_icon_folder, "rotate.png"),
            5: os.path.join(left_panel_icon_folder, "reset.jpg"),
            6: os.path.join(left_panel_icon_folder, "rectangle.png"),
            7: os.path.join(left_panel_icon_folder, "oval.png"),
            8: os.path.join(left_panel_icon_folder, "polygon.png"),
        }

        # Create 8 buttons
        for i in range(1, 9):

            left_buttons = QPushButton()

            # size
            left_buttons.setFixedSize(40, 40)

            # icon
            left_buttons.setIcon(QIcon(left_panel_icon_paths[i]))
            left_buttons.setIconSize(QtCore.QSize(24, 24))

            # normal mouse
            if i == 1:
                left_buttons.clicked.connect(self.disable_move_mode)
            # add moving image to second button
            if i == 2:
                left_buttons.clicked.connect(self.enable_move_mode)
            # reset iamge positon
            # zoom button
            if i == 3:
                self.button3 = Button3(self, left_buttons)
            # rotate 90 option
            if i == 4:
                self.button_rotated_option = Button_rotated_option(self,left_buttons)
            # reset position, rotation and zoom to original state
            if i == 5:
                left_buttons.clicked.connect(self.reset_image_to_start_position)
            # draw rectangle annotations
            if i == 6:
                left_buttons.clicked.connect(self.enable_rectangle_drawing)
            # draw oval annotations
            if i == 7:
                left_buttons.clicked.connect(self.enable_oval_drawing)
            # draw polygon annotations
            if i == 8:
                self.button_polygon_option = Button_polygon_option(self,left_buttons)

            # style of button
            left_buttons.setStyleSheet("""
                QPushButton {
                    background-color: #ecf0f1;
                    border: 2px solid #2c3e50;
                    border-radius: 6px;
                }

                QPushButton:hover {
                    background-color: #bdc3c7;
                }

                QPushButton:pressed {
                    background-color: #95a5a6;
                }
            """)

            left_layout.addWidget(
                left_buttons,
                alignment=QtCore.Qt.AlignHCenter
            )

        left_layout.addStretch()
        left_panel.setLayout(left_layout)

        return left_panel

    def create_middle_panel(self):
        middle_panel = QFrame()
        middle_panel.setStyleSheet("background-color: #1abc9c;")

        image_layout = QVBoxLayout()
        middle_panel.setLayout(image_layout)

        # Add image to layout
        self.image = ButtonLogic()
        self.image.setText("...")

        image_layout.addWidget(self.image)

        # connect frames to frame slider
        self.frame_slider.valueChanged.connect(self.image.show_frame)

        # reset zoom if change image or frame
        self.frame_slider.valueChanged.connect(self.button3.reset_zoom)

        # upade name frame after change frame
        self.frame_slider.valueChanged.connect(self.update_frame_info)

        # connect undo history
        self.image.draw_rectangle.on_annotion_comit = self.button_ctrl_z.save_current_state_of_label

        return middle_panel

    # right_panel
    def create_right_panel(self):

        # set right panel
        self.right_panel_logic = Main_Right_Panel_Label_Info(self.image, self.image.label_log)

        # connect right panel to frame slider
        self.frame_slider.valueChanged.connect(self.right_panel_logic.refresh_all_objects_in_list)

        # add list after creating or not labels
        self.image.draw_rectangle.on_annotations_changed = self.right_panel_logic.refresh_all_objects_in_list

        # add to list new created label
        self.image.label_log.on_labels_changed = self.right_panel_logic.refresh_all_labels_in_list

        # first Refresh of lisst
        self.right_panel_logic.refresh_all_objects_in_list()
        self.right_panel_logic.refresh_all_labels_in_list()

        return self.right_panel_logic.get_widget()

   #create bootn palen with slider
    def create_bottom_panel(self):
        bottom_panel = QFrame()
        bottom_panel.setFixedHeight(80)
        bottom_panel.setStyleSheet("background-color: #244eff;")

        # Create button layout
        bottom_button_layout = QHBoxLayout()
        bottom_button_layout.setContentsMargins(5, 5, 5, 5)
        bottom_button_layout.setSpacing(8)
        bottom_panel.setLayout(bottom_button_layout)

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

      #folder of botton icon
        bottom_panel_icon_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "bottom_panel_icons"
        )

        #all path to slider ickons
        bottom_panel_icon_paths = {
            1: os.path.join(bottom_panel_icon_folder, "slider_L_f.png"),
            2: os.path.join(bottom_panel_icon_folder, "slider_L_10.png"),
            3: os.path.join(bottom_panel_icon_folder, "slider_L_1.png"),
            4: os.path.join(bottom_panel_icon_folder, "slider_R.png"),
            5: os.path.join(bottom_panel_icon_folder, "slider_R_1.png"),
            6: os.path.join(bottom_panel_icon_folder, "slider_R_10.png"),
            7: os.path.join(bottom_panel_icon_folder, "slider_R_f.png"),
            8: os.path.join(bottom_panel_icon_folder, "slot11.png"),#change
        }



        # frame_slider
        self.frame_slider = QSlider(QtCore.Qt.Horizontal)
        self.frame_slider.setFixedSize(250, 45)
        self.frame_slider.setMinimum(1)
        self.frame_slider.setMaximum(100)
        self.frame_slider.setValue(0)

        # frame_slider_input
        self.frame_slider_input = QLineEdit()
        self.frame_slider_input.setFixedSize(60, 45)
        self.frame_slider_input.setAlignment(QtCore.Qt.AlignCenter)
        self.frame_slider_input.setText("1")

        # name of info file style )
        self.info_label = QLabel("")
        self.info_label.setStyleSheet("color: white; font-size: 11px;")
        self.info_label.setAlignment(QtCore.Qt.AlignCenter)


        # qwigtet to info (contaner
        self.frame_info_slider_container = QWidget()
        frame_info_slider_container = QVBoxLayout()
        frame_info_slider_container.setContentsMargins(0, 0, 0, 0)
        frame_info_slider_container.setSpacing(2)
        frame_info_slider_container.addWidget(self.frame_slider)
        frame_info_slider_container.addWidget(self.info_label)
        self.frame_info_slider_container.setLayout(frame_info_slider_container)


        # add_button_slider_logick
        self.create_button_frame_slider()

        # top_mid_button
        for i in range(1, 8):
            top_mid_button = QPushButton()
            top_mid_button.setFixedSize(60, 45)
            top_mid_button.setIcon(QIcon(bottom_panel_icon_paths[i]))
            top_mid_button.setIconSize(QtCore.QSize(24, 24))
            top_mid_button.setStyleSheet(button_style)


            match i:
                #set value to start position
                case 1:
                    top_mid_button.clicked.connect(self.button_frame_slider.start_value)
                # subtract to slider value 1
                case 2:
                    top_mid_button.clicked.connect(self.button_frame_slider.down_10)
                # subtract to slider value 10
                case 3:
                    top_mid_button.clicked.connect(self.button_frame_slider.down_1)
                #add to slider value 1
                case 5:
                    top_mid_button.clicked.connect(self.button_frame_slider.up_1)
                # add to slider value 10
                case 6:
                    top_mid_button.clicked.connect(self.button_frame_slider.up_10)
                # set value to max position
                case 7:
                    top_mid_button.clicked.connect(self.button_frame_slider.max_value)

            bottom_button_layout.addWidget(top_mid_button)
            bottom_button_layout.addStretch()

            bottom_button_layout.addWidget(self.frame_info_slider_container)
            bottom_button_layout.addWidget(self.frame_slider_input)
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


        return bottom_panel

    #Find file
    def find_image(self):
        file_path, filter = (QFileDialog.getOpenFileNames
            (self,
            "Selec image(s) or video","","Media (*.png *.jpg *.jpeg *.bmp *.mp4 *.avi *.mov *.mkv)")
            )

        if file_path:
            self.load_image_to_gui(file_path)

    # Load image
    def load_image_to_gui(self, file_paths):

        # wideo format
        video_extensions = (".mp4", ".avi", ".mov", ".mkv")

        # if is wideo or image
        first_file = file_paths[0]

        # if is wideo or image
        if first_file.lower().endswith(video_extensions):
            self.image.load_video(first_file)
        else:
            self.image.load_images(file_paths)

        # reest zoom if new image is load
        self.button3.reset_zoom()  # work ?

        # clear undo histroy if is new file
        self.button_ctrl_z.clear_saved_snapshots()

        # set   frame_slider to max number of frames
        count_frame = self.image.get_frame_count()
        self.frame_slider.setMinimum(1)
        self.frame_slider.setMaximum(max(count_frame, 1))
        self.frame_slider.setValue(1)

        #updae frame if is areldt
        self.update_frame_info()

    #Add top menu
    def add_menu(self):
        menu_first_bar = self.menuBar()


        file_menu = menu_first_bar.addMenu("File")

        first_action = QAction("Find file", self)
        first_action.triggered.connect(self.find_image)

        file_menu.addAction(first_action)

        #option to save all project
        menu_action_save_project = QAction("Save project", self)
        menu_action_save_project.triggered.connect(self.save_project_to_files)

        file_menu.addAction(menu_action_save_project)

    #save project fuction
    def save_project_to_files(self):

        #chose path to save
        json_file_path, selected_filter = QFileDialog.getSaveFileName(
            self, "Save project", "", "JSON Files (*.json)"
        )

        #user quit to chose option
        if not json_file_path:
            return

        #add .json if user not pint this
        if not json_file_path.lower().endswith(".json"):
            json_file_path += ".json"


        saved_project_logic = Saved_project(self.image)
        #save and catch error masage for later
        save_successful, error_message = saved_project_logic.save_current_project_to_files(json_file_path)

    # enable mouse drag
    def enable_move_mode(self):
        self.image.enable_drag(True)
        self.draw_mode_enabled = False
        self.image.enable_draw_mode(False)

        # if move enable edit is unbale
        self.image.enable_edit_mode(False)

        #if move is enable oval is unable
        self.draw_oval_mode_enabled = False
        self.image.enable_oval_draw_mode(False)

        #if move is enable drawing polygon is unable
        self.button_polygon_option.polygon_option_deactivate()

    # diabale move
    def disable_move_mode(self):
        self.image.enable_drag(False)
        self.draw_mode_enabled = False
        self.image.enable_draw_mode(False)

        # enable edit mode if move is siable
        self.image.enable_edit_mode(True)

        #enable edit mode then unable oval drawing
        self.draw_oval_mode_enabled = False
        self.image.enable_oval_draw_mode(False)

        #enable edit mode then unable darwing polygon
        self.button_polygon_option.polygon_option_deactivate()

    def enable_rectangle_drawing(self):

        self.draw_mode_enabled = not self.draw_mode_enabled
        self.image.enable_draw_mode(self.draw_mode_enabled)

        if self.draw_mode_enabled:
            self.image.enable_drag(False)

            # cannot edit adnotation if adnotation is creating
            self.image.enable_edit_mode(False)

            #cannot create oval if rectangle is created
            self.draw_oval_mode_enabled = False
            self.image.enable_oval_draw_mode(False)

            #cannot create polygon if rectangle is created
            self.button_polygon_option.polygon_option_deactivate()

    #  enable/un enable drawing oval
    def enable_oval_drawing(self):

        self.draw_oval_mode_enabled = not self.draw_oval_mode_enabled
        self.image.enable_oval_draw_mode(self.draw_oval_mode_enabled)

        if self.draw_oval_mode_enabled:
            self.image.enable_drag(False)
            self.image.enable_edit_mode(False)

           #canot draw rectangle if drawing oval
            self.draw_mode_enabled = False
            self.image.enable_draw_mode(False)

            #cannot draw polygon if darwaing oval
            self.button_polygon_option.polygon_option_deactivate()

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
        self.button_frame_slider = (Button_frame_slider
            (
            self.frame_slider,
            self.frame_slider_input
            ))

    #rotate image
    def rotate_image_to_left(self):
        self.image.rotate_image_to_left()

    #reset image to start pozition and zoom and angle
    def reset_image_to_start_position(self):
        self.image.reset_image_to_start_position()
        self.button3.reset_zoom()

        # instant refresh (only button need)
        self.image.repaint()

    # updae frame info
    def update_frame_info(self):
        self.info_label.setText(self.image.get_current_frame_info())