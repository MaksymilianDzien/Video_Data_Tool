from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import (
    QAction, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QPushButton, QMessageBox)
from core.Load_labels_csv import Load_labels_csv


class Extra_menus:

    #change
    about_title = "About"
    about_text = (
        "Simple GUI - annotation tool\n\n"
        "Rectangle, oval, polygon and magic wand annotations,\n"
        "labels, frames of video / image sequence.\n\n"
        "Author: ")

    #image formats
    open_file_images_formats = (".png", ".jpg", ".jpeg", ".bmp")
    #video formats
    open_file_video_formats = (".mp4", ".avi", ".mov", ".mkv")

    open_file_short_info = "png, jpg, mp4, ..."

    def __init__(self, extra_main_window):

        #main window of program
        self.extra_main_window = extra_main_window

        self.extra_menu_1 = None
        self.extra_menu_2 = None
        self.extra_menu_3 = None
        self.extra_menu_4 = None
        self.extra_menu_5 = None
        self.extra_menu_6 = None

    #add menu to bar in gui
    def add_extra_menus_to_bar(self, extra_menu_bar):

        #menu 1 file options
        self.extra_menu_1 = extra_menu_bar.addMenu("File")
        self.add_options_to_menu(self.extra_menu_1, self.file_options())

        #menu 2 edit options
        self.extra_menu_2 = extra_menu_bar.addMenu("Edit")
        self.add_options_to_menu(self.extra_menu_2, self.edit_options())

        #menu 3 image options
        self.extra_menu_3 = extra_menu_bar.addMenu("Image")
        self.add_options_to_menu(self.extra_menu_3, self.image_frame_options())

        #menu 4 draw options
        self.extra_menu_4 = extra_menu_bar.addMenu("Draw")
        self.add_options_to_menu(self.extra_menu_4, self.draw_annotation_options())

        #menu 5 annotation options
        self.extra_menu_5 = extra_menu_bar.addMenu("Annotation")
        self.add_options_to_menu(self.extra_menu_5, self.annotation_options())

        #menu 6 help options
        self.extra_menu_6 = extra_menu_bar.addMenu("Help")
        self.add_options_to_menu(self.extra_menu_6, self.help_options())

    #add list of options to menu
    def add_options_to_menu(self, menu, menu_options):

        for menu_option in menu_options:

            #separator
            if menu_option is None:
                menu.addSeparator()
                continue

            #set option text and function
            option_text, option_function = menu_option[0], menu_option[1]
            option_tooltip = menu_option[2] if len(menu_option) > 2 else None

            #submenu
            if isinstance(option_function, list):
                self.add_options_to_menu(menu.addMenu(option_text), option_function)
                continue

            #create QAction
            option_action = QAction(option_text, self.extra_main_window)

            #tooltip
            if option_tooltip:
                option_action.setToolTip(option_tooltip)
                menu.setToolTipsVisible(True)

            #connect function
            option_action.triggered.connect(option_function)
            menu.addAction(option_action)

    #file options
    def file_options(self):

        main_window = self.extra_main_window

        return [
            #all file options
            (f"Open file(s)  ({self.open_file_short_info})", lambda: main_window.find_image(),
                "Supported formats:\n"
                "Images: " + "  ".join(self.open_file_images_formats) + "\n"
                "Video: " + "  ".join(self.open_file_video_formats)),
            ("Open image sequence...", lambda: main_window.find_image_sequence()),
            None,
            ("Save project", lambda: main_window.save_project_to_files()),
            ("Load project", lambda: main_window.load_project_from_file()),
            None,
            ("Import annotations", [
                ("COCO 1.0 (.json)", lambda: main_window.import_annotations_from_format("coco")),
                ("YOLO 1.1 / Ultralytics (folder or .zip)", lambda: main_window.import_annotations_from_format("yolo")),
                ("PASCAL VOC 1.1 (folder or .zip)", lambda: main_window.import_annotations_from_format("voc")),
            ]),
            ("Load labels from CSV...", lambda: Load_labels_csv(main_window.image).load_labels_from_csv()),
            None,
            ("Exit", lambda: main_window.close()),
        ]

    #edit options
    def edit_options(self):

        main_window = self.extra_main_window

        return [
            #all edit options
            ("Undo\tCtrl+Z", lambda: main_window.button_ctrl_z.undo_current_frame()),
            ("Redo\tCtrl+D", lambda: main_window.button_ctrl_d.redo_current_frame()),
            None,
            ("Copy annotation\tCtrl+C", lambda: main_window.copy_paste_annotations.copy_selected_annotations()),
            ("Paste annotation\tCtrl+V", lambda: main_window.copy_paste_annotations.paste_annotations()),
            None,
            ("Delete selected\tBackspace", lambda: main_window.right_panel_logic.shortcut_delete_selected()),
        ]

    #image option
    def image_frame_options(self):

        main_window = self.extra_main_window

        #all image options
        return [
            #button 1  normal mouse
            ("Normal mouse mode\tCtrl", lambda: main_window.disable_move_mode()),
            #button 2  move image
            ("Move image", lambda: main_window.enable_move_mode()),
            #button 3  zoom
            ("Zoom", [
                ("Zoom tool\tZ", lambda: main_window.button3.toggle_zoom_mode()),
                ("Zoom in", self.zoom_in_from_menu),
                ("Zoom out", self.zoom_out_from_menu),
            ]),
            #button 4  rotate
            ("Rotate", [
                ("Rotate left\t,", lambda: main_window.image.rotate_image_to_left()),
                ("Rotate right\t.", lambda: main_window.image.rotate_image_to_right()),
            ]),
            #button 5  reset position, rotation and zoom
            ("Reset to start position\tCtrl+Space", lambda: main_window.reset_image_to_start_position()),
            None,
            #frames (the same as buttons in bottom panel)
            ("Go to frame", [
                ("First frame\tShift+Left", lambda: main_window.button_frame_slider.start_value()),
                ("Back 10 frames\tCtrl+Left", lambda: main_window.button_frame_slider.down_10()),
                ("Back 1 frame\tLeft", lambda: main_window.button_frame_slider.down_1()),
                ("Play / Stop\tSpace", lambda: main_window.button_frame_slider.play_frames()),
                ("Forward 1 frame\tRight", lambda: main_window.button_frame_slider.up_1()),
                ("Forward 10 frames\tCtrl+Right", lambda: main_window.button_frame_slider.up_10()),
                ("Last frame\tShift+Right", lambda: main_window.button_frame_slider.max_value()),
            ]),
        ]

    #draw option
    def draw_annotation_options(self):

        main_window = self.extra_main_window

        return [
            #drawing - same as buttons in left panel
            ("Rectangle\tR", lambda: main_window.enable_rectangle_drawing()),
            ("Oval\tO", lambda: main_window.enable_oval_drawing()),
            ("Polygon\tP", lambda: main_window.button_polygon_option.toggle_polygon_mode()),
            ("Magic wand", lambda: main_window.button_magic_wand.toggle_wand_mode()),
        ]

    #annotation options
    def annotation_options(self):

        main_window = self.extra_main_window
        #all annotation options
        return [
            ("Show / Hide\tV", lambda: main_window.right_panel_logic.shortcut_toggle_visible()),
            ("Lock / Unlock\tL", lambda: main_window.right_panel_logic.shortcut_toggle_locked()),
            ("Pin / Unpin\tM", lambda: main_window.right_panel_logic.shortcut_toggle_pinned()),
            ("Layer", [
                ("Bring to front\tCtrl+Up", lambda: main_window.right_panel_logic.shortcut_layer_of_selected("to_front")),
                ("Bring forward\tUp", lambda: main_window.right_panel_logic.shortcut_layer_of_selected("forward")),
                ("Send backward\tDown", lambda: main_window.right_panel_logic.shortcut_layer_of_selected("backward")),
                ("Send to back\tCtrl+Down", lambda: main_window.right_panel_logic.shortcut_layer_of_selected("to_back")),
            ]),
            None,
            ("Propagate", self.propagate_selected),
            ("Rename label", self.rename_selected_label),
            None,
            ("Delete\tBackspace", lambda: main_window.right_panel_logic.shortcut_delete_selected()),
        ]

    #help options
    def help_options(self):

        return [
            ("Shortcuts", self.shortcuts_table),
            ("About", self.about_dialog),
        ]

    #propagate selected annotation
    def propagate_selected(self):

        right_panel_logic = self.extra_main_window.right_panel_logic

        selected_annotation = right_panel_logic.get_selected_annotation()
        if selected_annotation is not None:
            right_panel_logic.copy_and_propagate.propagate_annotation(selected_annotation)
            return

        selected_label = right_panel_logic.get_selected_label()
        if selected_label is not None:
            right_panel_logic.copy_and_propagate.propagate_label(selected_label)
            return

        self.nothing_selected_message("Propagate")

    #rename label of selected annotation
    def rename_selected_label(self):

        right_panel_logic = self.extra_main_window.right_panel_logic

        selected_annotation = right_panel_logic.get_selected_annotation()
        if selected_annotation is not None:

            #annotation without label
            if selected_annotation.get("label_id") is None:
                QMessageBox.information(self.extra_main_window, "Rename label", "Selected annotation has no label.")
                return

            right_panel_logic.rename_label(selected_annotation["label_id"])
            return

        selected_label = right_panel_logic.get_selected_label()
        if selected_label is not None:
            right_panel_logic.rename_label(selected_label["id"])
            return

        self.nothing_selected_message("Rename label")

    #message if nothing is selected
    def nothing_selected_message(self, message_title):

        QMessageBox.information(self.extra_main_window, message_title, "Select an annotation or a label first.")

    #window About
    def about_dialog(self):

        QMessageBox.about(self.extra_main_window, self.about_title, self.about_text)

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