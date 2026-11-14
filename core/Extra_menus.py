from PyQt5.QtCore import Qt
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

        #menu 1, 2, 3 empty
        self.extra_menu_1 = extra_menu_bar.addMenu("1")
        self.extra_menu_2 = extra_menu_bar.addMenu("2")
        self.extra_menu_3 = extra_menu_bar.addMenu("3")

        #menu 4
        self.extra_menu_4 = extra_menu_bar.addMenu("4")

        # only Shortcuts option
        menu_action_shortcuts = QAction("Shortcuts", self.extra_main_window)
        #connect Shortcuts table
        menu_action_shortcuts.triggered.connect(self.shortcuts_table)

        self.extra_menu_4.addAction(menu_action_shortcuts)

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