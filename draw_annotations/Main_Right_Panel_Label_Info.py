from PyQt5.QtWidgets import QFrame, QVBoxLayout, QTabWidget, QListWidget, QListWidgetItem


class Main_Right_Panel_Label_Info:

    #width of info label
    info_labels_width = 300

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

            object_id = current_annotation["id"]

            # from label id to name if is not none then ""
            label_id = current_annotation["label_id"]
            label_text = self.current_label_obiect.get_label_name(label_id) if label_id is not None else "(no label)"

            list_of_item = f"{object_id}: {label_text}"

            #add object to item
            self.list_of_object.addItem(QListWidgetItem(list_of_item))

    # Refresh list of labes (if exist in list)
    def refresh_all_labels_in_list(self):

        self.list_of_labels.clear()

        # current_labels
        for current_label in self.current_label_obiect.current_labels:
            self.list_of_labels.addItem(QListWidgetItem(current_label["name"]))