from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QTabWidget, QListWidget, QListWidgetItem,
    QWidget, QPushButton, QLabel
)


class Main_Right_Panel_Label_Info:

    #width of info label
    info_labels_width = 300

    #size of right icon
    size_of_icon = 22

    def __init__(self, annotated_widget, current_label_obiect):

        # set image wiget (buuton 2 logick)
        self.annotated_widget = annotated_widget

        # set label object eqals
        self.current_label_obiect = current_label_obiect

        # set frame of right panel
        self.main_right_panel = QFrame()
        self.main_right_panel.setFixedWidth(self.info_labels_width)
        self.main_right_panel.setStyleSheet("background-color: #f1c40f;")

        # tabls
        self.object_and_labels_tabs = QTabWidget()

        # create list of id object
        self.list_of_object = QListWidget()
        self.object_and_labels_tabs.addTab(self.list_of_object, "Objects")

        # create list of labes
        self.list_of_labels = QListWidget()
        self.object_and_labels_tabs.addTab(self.list_of_labels, "Labels")

        # layaout of panel
        main_layout_of_right_panel = QVBoxLayout()
        main_layout_of_right_panel.setContentsMargins(0, 0, 0, 0)
        main_layout_of_right_panel.addWidget(self.object_and_labels_tabs)
        self.main_right_panel.setLayout(main_layout_of_right_panel)

    # getter to return right wighet to main gui
    def get_widget(self):
        return self.main_right_panel

    # Refresh list of oject
    def refresh_all_objects_in_list(self):

        #clear current list of annotations
        self.list_of_object.clear()

        #set annotations
        current_frame_index = self.annotated_widget.index_frame
        current_frame_annotations = self.annotated_widget.draw_rectangle.fream_annotation.get(current_frame_index, [])

        # set annotations in list after creatrion (with id)
        for current_annotation in current_frame_annotations:

            #createn wighet for id  name and option of annotaion
            list_widget_item = QListWidgetItem()
            concurrent_row_widget = self.create_object_row_widget(current_annotation)
            list_widget_item.setSizeHint(concurrent_row_widget.sizeHint())

            #add to litems
            self.list_of_object.addItem(list_widget_item)
            self.list_of_object.setItemWidget(list_widget_item, concurrent_row_widget)

    #crate row annotation
    def create_object_row_widget(self, curent_annotation):

        #create new widget (right row)
        annotation_row_widget = QWidget()
        #set laout
        annotation_row_layout = QHBoxLayout()
        annotation_row_layout.setContentsMargins(4, 2, 4, 2)
        annotation_row_layout.setSpacing(4)
        #add layout to widged
        annotation_row_widget.setLayout(annotation_row_layout)

        #set id and name of label
        object_id = curent_annotation["id"]
        label_id = curent_annotation["label_id"]
        label_text = self.current_label_obiect.get_label_name(label_id) if label_id is not None else "(no label)"

        #add to widget
        text_label = QLabel(f"{object_id}: {label_text}")
        annotation_row_layout.addWidget(text_label)

        #Stretch row
        annotation_row_layout.addStretch()

        #first button vislibity annation
        visibility_annotation_button = QPushButton()
        visibility_annotation_button.setFixedSize(self.size_of_icon, self.size_of_icon)
        visibility_annotation_button.setFlat(True)

        self.visibility_icon_button(visibility_annotation_button, curent_annotation.get("visible", True))

        #callback to viablie fuction
        visibility_annotation_button.clicked.connect(
            lambda checked=False, current_annotation=curent_annotation, current_button=visibility_annotation_button:
            self.current_all_annotation_visibility(current_annotation, current_button)
        )

        #add button to widget
        annotation_row_layout.addWidget(visibility_annotation_button)

        #second button lock annotation
        locked_annotation_button = QPushButton()
        locked_annotation_button.setFixedSize(self.size_of_icon, self.size_of_icon)
        locked_annotation_button.setFlat(True)

        self.lock_icon_button(locked_annotation_button, curent_annotation.get("locked", False))

        #callback to locked fuction
        locked_annotation_button.clicked.connect(
            lambda checked=False, current_annotation=curent_annotation, current_button=locked_annotation_button:
            self.current_all_annotation_lock(current_annotation, current_button)
        )

        #add button to widget
        annotation_row_layout.addWidget(locked_annotation_button)

        #third button pin annotation
        pinned_annotation_button = QPushButton()
        pinned_annotation_button.setFixedSize(self.size_of_icon, self.size_of_icon)
        pinned_annotation_button.setFlat(True)

        self.pin_icon_button(pinned_annotation_button, curent_annotation.get("pinned", False))

        #callback to pin fuction
        pinned_annotation_button.clicked.connect(
            lambda checked=False, current_annotation=curent_annotation, current_button=pinned_annotation_button:
            self.current_all_annotation_pin(current_annotation, current_button)
        )

        #add button to widget
        annotation_row_layout.addWidget(pinned_annotation_button)

       #1 button not yet
        #futrure add
        for _ in range(1):
            button_slot = QWidget()
            button_slot.setFixedSize(self.size_of_icon, self.size_of_icon)
            annotation_row_layout.addWidget(button_slot)

        return annotation_row_widget

    #redraw image and change visable flag
    def current_all_annotation_visibility(self, curent_annotation, button):
        #change flag
        curent_annotation["visible"] = not curent_annotation.get("visible", True)
        self.visibility_icon_button(button, curent_annotation["visible"])
        #redraw image
        self.annotated_widget.update()

    #set icon of visable
    def visibility_icon_button(self, current_button, is_visible):
        current_button.setText("V" if is_visible else "X")

    #redraw image and change locked flag
    def current_all_annotation_lock(self, curent_annotation, button):

        #change flag
        curent_annotation["locked"] = not curent_annotation.get("locked", False)
        self.lock_icon_button(button, curent_annotation["locked"])

        #if anntaion is selected then clear select and handers
        edit_current_anotation = self.annotated_widget.edit_current_anotation
        if edit_current_anotation.select_current_annotation is curent_annotation and curent_annotation["locked"]:
            edit_current_anotation.deselecte_edited_mode()

        #redraw image
        self.annotated_widget.update()

    #set icon of locked
    def lock_icon_button(self, current_button, is_locked):
        current_button.setText("L" if is_locked else "U")

    #redraw image and change pinned flag
    def current_all_annotation_pin(self, curent_annotation, button):

        #change flag
        curent_annotation["pinned"] = not curent_annotation.get("pinned", False)
        self.pin_icon_button(button, curent_annotation["pinned"])

        #if is pin then stop move annotaion
        edit_current_anotation = self.annotated_widget.edit_current_anotation
        if curent_annotation["pinned"]:
            edit_current_anotation.if_pinned_then_cancel_move(curent_annotation)

        #redraw image
        self.annotated_widget.update()

    #set icon of pinned
    def pin_icon_button(self, current_button, is_pinned):
        current_button.setText("P" if is_pinned else "F")

    # Refresh list of labes (if exist in list)
    def refresh_all_labels_in_list(self):

        self.list_of_labels.clear()

        # current_labels
        for current_label in self.current_label_obiect.current_labels:
            self.list_of_labels.addItem(QListWidgetItem(current_label["name"]))