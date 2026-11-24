from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QPoint


class Button_rotated_option:

    # size of popup buttons (L i R)
    sub_buttons_size = 40

    def __init__(self, current_main_window, main_rotation_button):

        # main window
        self.current_main_window = current_main_window

        # left main button 4
        self.main_rotation_button = main_rotation_button
        #set in button toggle/popup
        self.main_rotation_button.clicked.connect(self.popup_or_toggle_widget)

        #created mini widget for small buttons
        self.popup_toggle_widget = None
        self.create_right_left_widget()


    #crated mini widget for right or left button
    def create_right_left_widget(self):

        #close when is not cliked
        self.popup_toggle_widget = QWidget(None, Qt.Popup)

        #set style
        layout_of_widget = QHBoxLayout()
        layout_of_widget.setContentsMargins(4, 4, 4, 4)
        layout_of_widget.setSpacing(4)
        self.popup_toggle_widget.setLayout(layout_of_widget)

        #same style as gui
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

        #left button
        left_rotate_button = QPushButton("L")
        left_rotate_button.setFixedSize(self.sub_buttons_size, self.sub_buttons_size)
        left_rotate_button.setStyleSheet(button_style)
        left_rotate_button.clicked.connect(self.rotate_left)

        #right button
        right_rotate_button = QPushButton("R")
        right_rotate_button.setFixedSize(self.sub_buttons_size, self.sub_buttons_size)
        right_rotate_button.setStyleSheet(button_style)
        right_rotate_button.clicked.connect(self.rotate_right)

        #add button do widget
        layout_of_widget.addWidget(left_rotate_button)
        layout_of_widget.addWidget(right_rotate_button)

    # toggle or popup widget
    def popup_or_toggle_widget(self):

        # if is visible then close
        if self.popup_toggle_widget.isVisible():
            self.popup_toggle_widget.hide()
            return

        #set position of widget under main button
        current_button_position = self.main_rotation_button.mapToGlobal(QPoint(0, self.main_rotation_button.height()))
        self.popup_toggle_widget.move(current_button_position)
        self.popup_toggle_widget.show()

    #rotate left
    def rotate_left(self):
        self.current_main_window.image.rotate_image_to_left()
        self.popup_toggle_widget.hide()

    #rotate right
    def rotate_right(self):
        self.current_main_window.image.rotate_image_to_right()
        self.popup_toggle_widget.hide()