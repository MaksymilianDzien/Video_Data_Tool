from PyQt5.QtWidgets import QInputDialog


class Button_polygon_option:

    #default points of polygon
    default_count_of_point_option = 4
    #min points of polygon
    min_points_of_polygon = 3
    #max point of polygon
    max_points_of_polygon = 20

    #main self image (button
    def __init__(self, main_window, polygon_option_button):

        #main window (same as button 3 and ctr z )
        self.main_window = main_window

        #connect button to toggle_polygon_mode
        self.polygon_option_button = polygon_option_button
        self.polygon_option_button.clicked.connect(self.toggle_polygon_mode)

        #set if drawing is enable
        self.drawing_is_enable = False

    #window witch chose points of polyfon
    def toggle_polygon_mode(self):

        #if is eanble then disable
        if self.drawing_is_enable:
            self.polygon_option_deactivate()
            return

        #get Input Dialog witch init option and ask for polygon points
        polygon_point, ok = QInputDialog.getInt(
            self.polygon_option_button, "Number of points", "Enter the number of polygon points:",
            self.default_count_of_point_option, self.min_points_of_polygon, self.max_points_of_polygon
        )

        #if is not ok retrun
        if not ok:
            return

        main_window = self.main_window


        #exclusion of other modes (the same as rectangle)
        main_window.image.enable_drag(False)
        main_window.image.enable_edit_mode(False)

        main_window.draw_mode_enabled = False
        main_window.image.enable_draw_mode(False)

        main_window.draw_oval_mode_enabled = False
        main_window.image.enable_oval_draw_mode(False)

        self.drawing_is_enable = True
        main_window.image.enable_polygon_draw_mode(True, polygon_point)

    #deactivate if change optinon or change button
    def polygon_option_deactivate(self):
        self.drawing_is_enable = False
        self.main_window.image.enable_polygon_draw_mode(False)