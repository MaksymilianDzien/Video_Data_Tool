from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import (
    QAction, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QPushButton)


class Extra_menus:

    def __init__(self, extra_main_window):

        #main window of program
        self.extra_main_window = extra_main_window

        #create extra 4 menus
        self.extra_menu_1 = None
        self.extra_menu_2 = None
        self.extra_menu_3 = None
        self.extra_menu_4 = None

    #add menu to bar in gui
    def add_extra_menus_to_bar(self, extra_menu_bar):

        #menu 1 frame options
        self.extra_menu_1 = extra_menu_bar.addMenu("Frame")
        self.image_frame_options()

        #menu 2 draw annotation options
        self.extra_menu_2 = extra_menu_bar.addMenu("Draw annotation")
        self.draw_annotation_options()

        #menu 3 empty
        self.extra_menu_3 = extra_menu_bar.addMenu("3")

        #menu 4
        self.extra_menu_4 = extra_menu_bar.addMenu("4")

        # only Shortcuts option
        menu_action_shortcuts = QAction("Shortcuts", self.extra_main_window)
        #connect Shortcuts table
        menu_action_shortcuts.triggered.connect(self.shortcuts_table)

        self.extra_menu_4.addAction(menu_action_shortcuts)

    #frame option
    def image_frame_options(self):

        main_window = self.extra_main_window

        #(name in menu, function), None = separator
        image_frame_options = [
            #button 1  normal mouse
            ("Normal mouse mode", lambda: main_window.disable_move_mode()),
            #button 2  move image
            ("Move frame", lambda: main_window.enable_move_mode()),
            None,
            #button 3  zoom in / zoom out
            ("Zoom in", self.zoom_in_from_menu),
            ("Zoom out", self.zoom_out_from_menu),
            None,
            #button 4  rotate
            ("Rotate left", lambda: main_window.image.rotate_image_to_left()),
            ("Rotate right", lambda: main_window.image.rotate_image_to_right()),
            None,
            #button 5  reset position, rotation and zoom
            ("Reset to start position", lambda: main_window.reset_image_to_start_position()),
        ]

        for image_frame_option in image_frame_options:

            #separator
            if image_frame_option is None:
                self.extra_menu_1.addSeparator()
                continue

            #set option text and function
            option_text, option_function = image_frame_option
            #create QAction
            option_action = QAction(option_text, main_window)
            #connect function
            option_action.triggered.connect(option_function)
            self.extra_menu_1.addAction(option_action)

    #draw annotation option
    def draw_annotation_options(self):

        main_window = self.extra_main_window

        #(name in menu, function), None = separator
        draw_annotation_menu_options = [
            #drawing - same as buttons in left panel
            ("Draw rectangle", lambda: main_window.enable_rectangle_drawing()),
            ("Draw oval", lambda: main_window.enable_oval_drawing()),
            ("Draw polygon", lambda: main_window.button_polygon_option.toggle_polygon_mode()),
            ("Magic wand", lambda: main_window.button_magic_wand.toggle_wand_mode()),
            None,
            #undo / redo - same as Ctrl + Z / Ctrl + D buttons
            ("Undo (Ctrl + Z)", lambda: main_window.button_ctrl_z.undo_current_frame()),
            ("Redo (Ctrl + D)", lambda: main_window.button_ctrl_d.redo_current_frame()),
        ]

        for draw_annotation_option in draw_annotation_menu_options:

            #separator
            if draw_annotation_option is None:
                self.extra_menu_2.addSeparator()
                continue

            #set option text and function
            option_text, option_function = draw_annotation_option
            option_action = QAction(option_text, main_window)
            option_action.triggered.connect(option_function)
            self.extra_menu_2.addAction(option_action)

    #zoom in
    def zoom_in_from_menu(self):
        self.zoom_from_menu(self.extra_main_window.button3.step_zoom)

    #zoom out
    def zoom_out_from_menu(self):
        self.zoom_from_menu(1 / self.extra_main_window.button3.step_zoom)

    #zoom in menu (in frame)
    def zoom_from_menu(self, zoom_factor):

        #set zoom and image widget
        image_widget = self.extra_main_window.image
        zoom_button = self.extra_main_window.button3

        #no frame loaded
        if image_widget.original_iamge is None:
            return

        #center of the visible window
        zoom_point = QPoint(image_widget.width() // 2, image_widget.height() // 2)

        #if there is no frame in the center, use the center of the frame
        if not zoom_button.point_is_inside_frame(zoom_point):
            zoom_point = QPoint(
                image_widget.positon.x() + image_widget.original_iamge.width() // 2,
                image_widget.positon.y() + image_widget.original_iamge.height() // 2)

        zoom_button.zoom_image(zoom_point, zoom_factor)

    #show shortcuts table
    def shortcuts_table(self):

        shortcuts_dialog = Shortcuts_table(self.extra_main_window)
        shortcuts_dialog.exec_()


#Table Shortcuts
class Shortcuts_table(QDialog):

    #kolumns
    table_headers = ("Shortcut", "Action", "Where")

    #size of table
    table_width = 620
    table_height = 520

    def __init__(self, table_parent_window):
        super().__init__(table_parent_window)


        #set title and size
        self.setWindowTitle("Keyboard shortcuts")
        self.resize(self.table_width, self.table_height)

        #layout of table
        table_layout = QVBoxLayout()
        self.setLayout(table_layout)

        #get table values
        shortcuts_list = get_shortcuts_list()
        self.shortcuts_table_widget = QTableWidget(len(shortcuts_list), len(self.table_headers))
        self.shortcuts_table_widget.setHorizontalHeaderLabels(self.table_headers)

        #only rows
        self.shortcuts_table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.shortcuts_table_widget.setSelectionMode(QAbstractItemView.NoSelection)
        self.shortcuts_table_widget.verticalHeader().setVisible(False)
        self.shortcuts_table_widget.setAlternatingRowColors(True)

        #fill all rows
        for row_index, shortcut_row in enumerate(shortcuts_list):
            for column_index, cell_text in enumerate(shortcut_row):
                self.shortcuts_table_widget.setItem(row_index, column_index, QTableWidgetItem(cell_text))

        #size of header
        table_header = self.shortcuts_table_widget.horizontalHeader()
        table_header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        table_header.setSectionResizeMode(1, QHeaderView.Stretch)
        table_header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        table_layout.addWidget(self.shortcuts_table_widget)

        #close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        table_layout.addWidget(close_button, alignment=Qt.AlignRight)


#all shortcuts
def get_shortcuts_list():
    return [

        #left panel
        ("R", "Draw rectangle (on / off)", "Image"),
        ("O", "Draw oval (on / off)", "Image"),
        ("P", "Draw polygon (on / off)", "Image"),
        ("Z", "Zoom tool - left click zoom in, right click zoom out ", "Image"),
        ("Ctrl + Space", "Reset image position, rotation and zoom", "Image"),
        (",", "Rotate image to the left", "Image"),
        (".", "Rotate image to the right", "Image"),
        ("Mouse wheel up / down", "Zoom in / out by 10% ", "Image"),
        ("Ctrl ", "Normal mouse mode ", "Image"),

        #copy / paste annotations
        ("Ctrl + C", "Copy selected annotation ", "Image"),
        ("Ctrl + V", "Paste copied annotation ", "Image"),

        #Magic wand
        ("Enter", "Finish magic wand polygon", "Magic wand"),
        ("Esc", "Cancel magic wand selection", "Magic wand"),

        #bottom panel
        ("Shift + Left", "Go to the first frame", "Bottom panel"),
        ("Ctrl + Left", "Go back 10 frames", "Bottom panel"),
        ("Left", "Go back 1 frame", "Bottom panel"),
        ("Space", "Play / stop playing frames", "Bottom panel"),
        ("Right", "Go forward 1 frame", "Bottom panel"),
        ("Ctrl + Right", "Go forward 10 frames", "Bottom panel"),
        ("Shift + Right", "Go to the last frame", "Bottom panel"),

        #right panel
        ("V", "Show / hide selected annotation or label", "Right panel"),
        ("L", "Lock / unlock selected annotation or label", "Right panel"),
        ("M", "Pin / unpin selected annotation or label", "Right panel"),
        ("Ctrl + Up", "Bring to front", "Right panel"),
        ("Up", "Bring forward", "Right panel"),
        ("Down", "Send backward", "Right panel"),
        ("Ctrl + Down", "Send to back", "Right panel"),
        ("Backspace", "Delete selected annotation or label", "Right panel"),
    ]