import copy
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from draw_annotations.More_option_copy_and_propagate import More_option_copy_and_propagate


class Copy_paste_annotations:

    def __init__(self, copy_main_window):

        #set main window
        self.copy_main_window = copy_main_window
        #image widget (ButtonLogic)
        self.copy_image_widget = copy_main_window.image

        #use the same copying logic as in "Make a copy".
        self.copy_and_propagate = More_option_copy_and_propagate(self.copy_image_widget)

        #clipboard
        self.copied_annotations = []

        #set shortcuts Ctrl + C and Ctrl + V
        self.copy_paste_all_shortcut()

    #get selected annotations on current frame
    def get_selected_annotations(self):

        edit_current_anotation = self.copy_image_widget.edit_current_anotation
        frame_index = self.copy_image_widget.index_frame
        frame_annotations = self.copy_image_widget.draw_rectangle.fream_annotation.get(frame_index, [])

        #1 annotation selected
        selected_annotation = edit_current_anotation.select_current_annotation
        if selected_annotation is not None:
            selected_annotations = [selected_annotation]
        else:
            #all annotations of label selected (right panel)
            selected_annotations = list(edit_current_anotation.select_annotations_in_group)

        #only annotations which are on the current frame
        return [annotation for annotation in selected_annotations
                if any(annotation is frame_annotation for frame_annotation in frame_annotations)]

    #Ctrl + C
    def copy_selected_annotations(self):

        selected_annotations = self.get_selected_annotations()

        #nothing selected - old clipboard stays
        if not selected_annotations:
            return

        self.copied_annotations = [copy.deepcopy(annotation) for annotation in selected_annotations]

    #Ctrl + V
    def paste_annotations(self):

        #nothing copied or no frames
        if not self.copied_annotations or len(self.copy_image_widget.All_frames) == 0:
            return

        frame_index = self.copy_image_widget.index_frame
        draw_rectangle = self.copy_image_widget.draw_rectangle

        #frame can have no list yet
        draw_rectangle.fream_annotation.setdefault(frame_index, [])

        new_annotations = self.copy_and_propagate.copy_annotations_in_same_frame(self.copied_annotations, frame_index)
        self.copy_and_propagate.finish_change()

        #new copy is selected
        edit_current_anotation = self.copy_image_widget.edit_current_anotation
        if edit_current_anotation.edit_of_annotation:
            if len(new_annotations) == 1:
                edit_current_anotation.select_annotation_right_panel(new_annotations[0], frame_index)
            else:
                edit_current_anotation.select_label_annotations_right_panel(new_annotations, frame_index)

    #shortcuts Ctrl + C and Ctrl + V
    def copy_paste_all_shortcut(self):

        self.shortcut_copy = QShortcut(QKeySequence("Ctrl+C"), self.copy_main_window)
        self.shortcut_copy.activated.connect(self.copy_selected_annotations)

        self.shortcut_paste = QShortcut(QKeySequence("Ctrl+V"), self.copy_main_window)
        self.shortcut_paste.activated.connect(self.paste_annotations)