from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

class Button_ctrl_d:

    def __init__(self, main_window, button_redo, button_ctrl_z):

        # main window
        self.main_window = main_window

        #set ctrl z to list
        self.button_ctrl_z = button_ctrl_z

        #connect button to redo (t.3)
        self.button_redo = button_redo
        self.button_redo.clicked.connect(self.redo_current_frame)

        #key shortcut button redo
        self.shortcut_redo_button = QShortcut(QKeySequence("Ctrl+D"), self.main_window)
        self.shortcut_redo_button.activated.connect(self.redo_current_frame)

    #redo curent frame
    def redo_current_frame(self):

        #if is not histroy yet then retrun
        if not self.button_ctrl_z.redo_history:
            return

        #set stage that is undone (last ctrl+z)
        current_next_state = self.button_ctrl_z.redo_history.pop()

        #set stage retrun to the ctrl + z history list
        self.button_ctrl_z.saved_history.append(current_next_state)

        #set rendo max
        if len(self.button_ctrl_z.saved_history) > self.button_ctrl_z.undo_step:
            self.button_ctrl_z.saved_history.pop(0)

        # refer to drawing rectangle
        current_draw_rectangle = self.main_window.image.draw_rectangle

        #restoring state from a copy
        current_draw_rectangle.fream_annotation = {
            frame_index: [dict(annotation) for annotation in annotations]
            for frame_index, annotations in current_next_state.items()}

        #clear select if is edited
        self.main_window.image.edit_current_anotation.deselecte_edited_mode()

        #redraw all frame
        self.main_window.image.repaint()

        #redraw right panel
        current_draw_rectangle.current_annotations_changed()