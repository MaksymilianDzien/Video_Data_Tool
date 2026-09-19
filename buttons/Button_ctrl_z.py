from turtledemo.clock import current_day


class Button_ctrl_z:

    #max undo step
    undo_step = 30

    def __init__(self, main_window, button_undo):

        # main window
        self.main_window = main_window

        #connect button to undo (t.2)
        self.button_undo = button_undo
        self.button_undo.clicked.connect(self.undo_current_frame)

        # set new table of saved annotation
        self.saved_history = []

    # sabe current state of annotaion
    def save_current_state_of_label(self):

        current_saved_annotation = self.main_window.image.draw_rectangle.fream_annotation

        # new diary  key id valies qReftf label ...
        snapshot_of_annotation = {
            frame_index: [dict(annotation) for annotation in annotations]
            for frame_index, annotations in current_saved_annotation.items()
        }

        #svaet to snapshot history
        self.saved_history.append(snapshot_of_annotation)

        # chek if is in range to max undo
        if len(self.saved_history) > self.undo_step:
            self.saved_history.pop(0)

    # clear all history
    def clear_saved_snapshots(self):
        self.saved_history = []

    # undo fuction
    def undo_current_frame(self):

        # if is not ini then just retrun
        if not self.saved_history:
            return


        # delete current state of frame
        self.saved_history.pop()

        # refer to drawing rectangle
        current_draw_rectangle = self.main_window.image.draw_rectangle


        #restoration previous_state
        if self.saved_history:
            previous_state = self.saved_history[-1]
            current_draw_rectangle.fream_annotation = {
                frame_index: [dict(annotation) for annotation in annotations]
                for frame_index, annotations in previous_state.items()
            }
        #if is epty or is not have last step
        else:
            current_draw_rectangle.fream_annotation = {}

        # repaint to current frame ( to see rezult)
        self.main_window.image.repaint()

        # change right palenl
        current_draw_rectangle.current_annotations_changed()