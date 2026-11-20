import copy
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLabel, QSpinBox, QDialogButtonBox, QMessageBox


#copy and propagate
class More_option_copy_and_propagate:

    #delaft frame propagate
    default_propagate_frames = 10

    #offset of copy in px
    offset_of_copy = 0

    def __init__(self, current_annotated_widget):

        #set widget ButtonLogic
        self.current_annotated_widget = current_annotated_widget

    #get current annotation object
    def get_draw_rectangle(self):
        return self.current_annotated_widget.draw_rectangle

    #get number of frame
    def get_frame_of_annotation(self, curent_annotation):

        for frame_index, frame_annotations in self.get_draw_rectangle().fream_annotation.items():
            if any(annotation is curent_annotation for annotation in frame_annotations):
                return frame_index
        #not find number return none
        return None

    #get all annotation of label in onle frame
    def get_annotations_of_label(self, curent_label, frame_index):

        frame_annotations = self.get_draw_rectangle().fream_annotation.get(frame_index, [])
        return [annotation for annotation in frame_annotations if annotation.get("label_id") == curent_label["id"]]

    #create new copy of annotation witch new id
    def copy_annotation(self, annotation, offset):

        draw_rectangle = self.get_draw_rectangle()

        #copy list of point polygon
        new_annotation = copy.deepcopy(annotation)
        new_annotation["id"] = draw_rectangle.next_annotation_id
        draw_rectangle.next_annotation_id += 1

        #off set
        if offset != 0:
            if new_annotation.get("type") == "polygon":
                for point in new_annotation["points"]:
                    point["x"] += offset
                    point["y"] += offset
            else:
                new_annotation["x"] += offset
                new_annotation["y"] += offset

        return new_annotation

    #copy annotation in same frame
    def copy_annotations_in_same_frame(self, annotations, frame_index):

        draw_rectangle = self.get_draw_rectangle()

        #annotation copy have same layer as main annotation
        sorted_sources = sorted(annotations, key=lambda annotation: annotation.get("layer", 1))

        #all old annotation one layer down
        for _ in sorted_sources:
            draw_rectangle.all_other_annotations__back(frame_index)

        new_annotations = []
        for index, source_annotation in enumerate(sorted_sources):
            new_annotation = self.copy_annotation(source_annotation, self.offset_of_copy)
            new_annotation["layer"] = min(index + 1, draw_rectangle.layers)
            draw_rectangle.fream_annotation[frame_index].append(new_annotation)
            new_annotations.append(new_annotation)

        return new_annotations

    #copy annotation in other frames  propagate
    def copy_annotations_to_frames(self, annotations, source_frame, from_frame, to_frame):

        draw_rectangle = self.get_draw_rectangle()
        added_annotations_count = 0

        for frame_index in range(from_frame, to_frame + 1):

            #skip current frame
            if frame_index == source_frame:
                continue

            #create list of annotation if not created
            frame_annotations = draw_rectangle.fream_annotation.setdefault(frame_index, [])

            #during propagation, the copy has the same layer and the same location as the source
            for source_annotation in annotations:
                frame_annotations.append(self.copy_annotation(source_annotation, 0))
                added_annotations_count += 1

        return added_annotations_count

    #window ask for frames range
    def ask_for_frames_range(self, window_title, text):

        total_frames = len(self.current_annotated_widget.All_frames)
        if total_frames == 0:
            return None


        #frame number as seen by the user
        current_frame_number = self.current_annotated_widget.index_frame + 1

        frames_dialog = QDialog(self.current_annotated_widget)
        frames_dialog.setWindowTitle(window_title)

        dialog_layout = QVBoxLayout(frames_dialog)
        dialog_layout.addWidget(QLabel(text))
        dialog_layout.addWidget(QLabel(f"Current frame: {current_frame_number} / {total_frames}"))

        #pola "od klatki" i "do klatki"
        from_frame_spin = QSpinBox()
        from_frame_spin.setRange(1, total_frames)
        from_frame_spin.setValue(min(current_frame_number + 1, total_frames))

        to_frame_spin = QSpinBox()
        to_frame_spin.setRange(1, total_frames)
        to_frame_spin.setValue(min(current_frame_number + self.default_propagate_frames, total_frames))

        #"From" cannot be greater than "to"
        to_frame_spin.setMinimum(from_frame_spin.value())
        from_frame_spin.setMaximum(to_frame_spin.value())
        from_frame_spin.valueChanged.connect(to_frame_spin.setMinimum)
        to_frame_spin.valueChanged.connect(from_frame_spin.setMaximum)

        frames_form = QFormLayout()
        frames_form.addRow("From frame:", from_frame_spin)
        frames_form.addRow("To frame:", to_frame_spin)
        dialog_layout.addLayout(frames_form)

        #ok and cancel button
        dialog_buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dialog_buttons.accepted.connect(frames_dialog.accept)
        dialog_buttons.rejected.connect(frames_dialog.reject)
        dialog_layout.addWidget(dialog_buttons)

        if frames_dialog.exec_() != QDialog.Accepted:
            return None

        #returning to numbering starting from 0
        return from_frame_spin.value() - 1, to_frame_spin.value() - 1

    #message when the cable has nothing on the current frame
    def show_no_annotations_message(self, window_title, curent_label):
        QMessageBox.information(
            self.current_annotated_widget, window_title,
            f"There are no annotations of label '{curent_label['name']}' on the current frame.")

    #save to ctrl + z history
    def finish_change(self):

        draw_rectangle = self.get_draw_rectangle()
        draw_rectangle.on_annotion_comit()
        draw_rectangle.current_annotations_changed()
        self.current_annotated_widget.update()


    #Make a copy annotation
    def make_copy_of_annotation(self, curent_annotation):

        frame_index = self.get_frame_of_annotation(curent_annotation)
        if frame_index is None:
            return

        new_annotations = self.copy_annotations_in_same_frame([curent_annotation], frame_index)
        self.finish_change()

        #new copy is selected
        edit_current_anotation = self.current_annotated_widget.edit_current_anotation
        if edit_current_anotation.edit_of_annotation:
            edit_current_anotation.select_annotation_right_panel(new_annotations[0], frame_index)

    #Make a copy label
    def make_copy_of_label(self, curent_label):

        frame_index = self.current_annotated_widget.index_frame
        source_annotations = self.get_annotations_of_label(curent_label, frame_index)

        if not source_annotations:
            self.show_no_annotations_message("Make a copy", curent_label)
            return

        new_annotations = self.copy_annotations_in_same_frame(source_annotations, frame_index)
        self.finish_change()

        #new copy is selected
        edit_current_anotation = self.current_annotated_widget.edit_current_anotation
        if edit_current_anotation.edit_of_annotation:
            edit_current_anotation.select_label_annotations_right_panel(new_annotations, frame_index)

    #Propagate annotation
    def propagate_annotation(self, curent_annotation):

        source_frame = self.get_frame_of_annotation(curent_annotation)
        if source_frame is None:
            return

        frames_range = self.ask_for_frames_range(
            "Propagate annotation",
            f"Annotation {curent_annotation['id']} will be copied to every frame in the range.")
        if frames_range is None:
            return

        from_frame, to_frame = frames_range
        added_annotations_count = self.copy_annotations_to_frames([curent_annotation], source_frame, from_frame, to_frame)

        #nothing added
        if added_annotations_count == 0:
            return

        self.finish_change()

    #Propagate label
    def propagate_label(self, curent_label):

        source_frame = self.current_annotated_widget.index_frame
        source_annotations = self.get_annotations_of_label(curent_label, source_frame)

        if not source_annotations:
            self.show_no_annotations_message("Propagate", curent_label)
            return

        frames_range = self.ask_for_frames_range(
            "Propagate label",
            f"{len(source_annotations)} annotation(s) of label '{curent_label['name']}' "
            f"will be copied to every frame in the range.")
        if frames_range is None:
            return

        from_frame, to_frame = frames_range
        added_annotations_count = self.copy_annotations_to_frames(source_annotations, source_frame, from_frame, to_frame)

        #nothing added
        if added_annotations_count == 0:
            return

        self.finish_change()