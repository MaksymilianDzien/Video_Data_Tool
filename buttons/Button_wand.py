from PyQt5.QtWidgets import QInputDialog


#left panel wand button
class Button_wand:


    #default tolerance
    default_wand_color_tolerance = 20

    #min tolerance
    min_tolerance = 1

    #max tolerance
    max_tolerance = 100

    #main window left panel button
    def __init__(self, wand_main_window, wand_button):

        #main window
        self.wand_main_window = wand_main_window


        #clicking the button turns the wand on/off
        self.magic_wand_button = wand_button
        self.magic_wand_button.clicked.connect(self.toggle_wand_mode)
        #set info
        self.magic_wand_button.setToolTip(
            "Magic wand: left click - add area, right click - remove area, Enter - create polygon, Esc - cancel"
        )

        #set drawin false
        self.drawing_is_enable = False

    #window with tolerance and wand activation
    def toggle_wand_mode(self):

        #if is enable then deactivate
        if self.drawing_is_enable:
            self.magic_wand_deactivate()
            return

        #ask about color tolerances
        tolerance, ok = QInputDialog.getInt(
            self.magic_wand_button, "Magic wand", "Enter the color tolerance (1 - 100):",
            self.default_wand_color_tolerance, self.min_tolerance, self.max_tolerance)

        #if not accept
        if not ok:
            return

        main_window = self.wand_main_window

        #disable other modes
        main_window.image.enable_drag(False)
        main_window.image.enable_edit_mode(False)

        main_window.draw_mode_enabled = False
        main_window.image.enable_draw_mode(False)

        main_window.draw_oval_mode_enabled = False
        main_window.image.enable_oval_draw_mode(False)

        main_window.button_polygon_option.polygon_option_deactivate()

        self.drawing_is_enable = True
        main_window.image.enable_magic_wand_draw_mode(True, tolerance)

    #deactivate wand
    def magic_wand_deactivate(self):
        self.drawing_is_enable = False
        self.wand_main_window.image.enable_magic_wand_draw_mode(False)