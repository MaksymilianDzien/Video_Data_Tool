import os
from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QTabWidget, QListWidget, QListWidgetItem,QWidget, QPushButton, QLabel, QMenu)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize


class Main_Right_Panel_Label_Info:

    #width of info label
    info_labels_width = 300

    #size of right icon
    size_of_icon = 22

    #height of one row
    height_of_row = 36

    #spacing bettwen rows
    spacing_of_row = 3


    #style of annotaion table (silmilar to left panel)
    row_frame_style = """
        QFrame#annotation_row_frame {
            background-color: #ecf0f1;
            border: 2px solid #2c3e50;
            border-radius: 3px;
        }
        QFrame#annotation_row_frame:hover {
            background-color: #bdc3c7;
        }
        QWidget {
            background: transparent;
        }
        QLabel {
            border: none;
            font-weight: bold;
        }
    """

    #style of list
    list_of_items_style = """
        QListWidget::item { background: transparent; }
        QListWidget::item:selected { background: transparent; }
        QListWidget::item:hover { background: transparent; }
    """

    def __init__(self, annotated_widget, current_label_obiect):

       #folder with panel panel ikons
        annotation_option_icon_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),"annotaion_option_icons")

        # icon visible/hidden paths
        self.visible_icon = os.path.join(annotation_option_icon_folder, "visible.png")
        self.hidden_icon = os.path.join(annotation_option_icon_folder, "hidden.png")

        # icon locked/unlocked paths
        self.locked_icon = os.path.join(annotation_option_icon_folder, "locked.png")
        self.unlocked_icon = os.path.join(annotation_option_icon_folder, "unlocked.png")

        # icon pinned/unpinned paths
        self.pinned_icon = os.path.join(annotation_option_icon_folder, "pinned.png")
        self.unpinned_icon = os.path.join(annotation_option_icon_folder, "unpinned.png")

       #icon of delete option
        self.delete_icon = os.path.join(annotation_option_icon_folder, "delete.png")

        #icon of back to last layer
        self.max_back_icon = os.path.join(annotation_option_icon_folder, "max_to_back.png")
        #icon of backward one layer
        self.one_backward_icon = os.path.join(annotation_option_icon_folder, "one_backward.png")
        #icon of forward one layer
        self.one_forward_icon = os.path.join(annotation_option_icon_folder, "one_forward.png")
        #icon of forward first layer
        self.max_front_icon = os.path.join(annotation_option_icon_folder, "max_to_front.png")

       #icon of more option
        self.more_option_icon = os.path.join(annotation_option_icon_folder, "more.png")

        # set image wiget (buuton 2 logick)
        self.annotated_widget = annotated_widget

        # set label object eqals
        self.current_label_obiect = current_label_obiect

        # set frame of right panel
        self.main_right_panel = QFrame()
        self.main_right_panel.setFixedWidth(self.info_labels_width)
        self.main_right_panel.setStyleSheet("background-color: #D7D7D7;")

        # tabls
        self.object_and_labels_tabs = QTabWidget()

        # create list of id object
        self.list_of_object = QListWidget()

        #set spacing and style of list of obieckt
        self.list_of_object.setSpacing(self.spacing_of_row)
        self.list_of_object.setStyleSheet(self.list_of_items_style)
        self.object_and_labels_tabs.addTab(self.list_of_object, "Objects")

        # create list of labes
        self.list_of_labels = QListWidget()
        # odstęp między ramkami i styl elementów listy labeli
        self.list_of_labels.setSpacing(self.spacing_of_row)
        self.list_of_labels.setStyleSheet(self.list_of_items_style)
        self.object_and_labels_tabs.addTab(self.list_of_labels, "Labels")

        # layaout of panel
        main_layout_of_right_panel = QVBoxLayout()
        main_layout_of_right_panel.setContentsMargins(0, 0, 0, 0)
        main_layout_of_right_panel.addWidget(self.object_and_labels_tabs)
        self.main_right_panel.setLayout(main_layout_of_right_panel)

    # getter to return right wighet to main gui
    def get_widget(self):
        return self.main_right_panel

    #create 4 button for more anntaion option
    def create_more_option_button(self, more_options_list):

        #set icon and size more option
        more_options_button = QPushButton()
        more_options_button.setIcon(QIcon(self.more_option_icon))
        more_options_button.setIconSize(QSize(self.size_of_icon, self.size_of_icon))
        #set size of button
        more_options_button.setFixedSize(self.size_of_icon, self.size_of_icon)
        #set style of this button
        more_options_button.setFlat(True)
        more_options_button.setStyleSheet("QPushButton { border: none; background: transparent; font-weight: bold; }")

        #if is cliked open more option menu
        more_options_button.clicked.connect(lambda checked=False, current_button=more_options_button:
            self.show_more_options_menu(current_button, more_options_list))

        #retun this more option button
        return more_options_button

    #show more option menu witch options
    def show_more_options_menu(self, more_option_button, more_options_list):

        #create new mini menu for annotaion option
        more_options_menu = QMenu()

        #new QAction menu option
        Qactions_with_functions = {}

        #add all option to list
        for more_option in more_options_list:

            #if is none add seprator to menu
            if more_option is None:
                more_options_menu.addSeparator()
                continue

            #set with icon and name
            more_option_icon_path, more_option_text, more_option_function = more_option
            option_action = more_options_menu.addAction(QIcon(more_option_icon_path), more_option_text)
            Qactions_with_functions[option_action] = more_option_function

        #menu is create from bottom left and retrun chose of menu
        more_option_chosen_action = more_options_menu.exec_(more_option_button.mapToGlobal(more_option_button.rect().bottomLeft()))

        #if chose any action call function of this action
        if more_option_chosen_action in Qactions_with_functions:
            Qactions_with_functions[more_option_chosen_action]()

    #create more option list of fuction
    def create_more_options_list(self, more_layer_function, more_delete_text, more_delete_function):
        return [
            # (1)max up
            (self.max_front_icon, "Bring to front", lambda: more_layer_function("to_front")),
            # (2)one up
            (self.one_forward_icon, "Bring forward", lambda: more_layer_function("forward")),
            # (3)one back
            (self.one_backward_icon, "Send backward", lambda: more_layer_function("backward")),
            # (4)max back
            (self.max_back_icon, "Send to back", lambda: more_layer_function("to_back")),
            # seperator
            None,
            # (5) delete
            (self.delete_icon, more_delete_text, more_delete_function),
        ]

    #reorder layer in frames
    def reorder_current_layer_in_frame(self, current_frame_annotations, is_selected, action_of_layer):

        #order annotaion in front (first layer)
        order_annotations = sorted(current_frame_annotations, key=lambda annotation: annotation.get("layer", 1))

        #if
        if not any(is_selected(annotation) for annotation in order_annotations):
            return

        if action_of_layer == "to_front":
            #add layer in fornt of list of annotaion
            order_annotations = (
                [annotation for annotation in order_annotations if is_selected(annotation)]
                + [annotation for annotation in order_annotations if not is_selected(annotation)])

        elif action_of_layer == "to_back":
            #one back in annotaion list
            order_annotations = (
                [annotation for annotation in order_annotations if not is_selected(annotation)]
                + [annotation for annotation in order_annotations if is_selected(annotation)])

        elif action_of_layer == "forward":
            #one to front to annotaion list
            for index in range(1, len(order_annotations)):
                if is_selected(order_annotations[index]) and not is_selected(order_annotations[index - 1]):
                    order_annotations[index - 1], order_annotations[index] = \
                        order_annotations[index], order_annotations[index - 1]

        elif action_of_layer == "backward":
            #add current layer to last value in annotaion list
            for index in range(len(order_annotations) - 2, -1, -1):
                if is_selected(order_annotations[index]) and not is_selected(order_annotations[index + 1]):
                    order_annotations[index + 1], order_annotations[index] = \
                        order_annotations[index], order_annotations[index + 1]

        #change all anntaion order in list in layers
        max_layer = self.annotated_widget.draw_rectangle.layers
        for index, annotation in enumerate(order_annotations):
            annotation["layer"] = min(index + 1, max_layer)

    #change annotaion layers ( 1 - 4 options in menu )
    def change_layers_of_annotations(self, curent_annotation, change_layer_action):

        #create new rectangle
        change_current_draw_rectangle = self.annotated_widget.draw_rectangle

        #find current annotaion in list ( is e)
        for for_frame_annotations in change_current_draw_rectangle.fream_annotation.values():
            if any(annotation is curent_annotation for annotation in for_frame_annotations):
                self.reorder_current_layer_in_frame(
                    for_frame_annotations,
                    lambda annotation: annotation is curent_annotation,change_layer_action)
                break

        #save ctrl + z history
        #redraw all
        self.finish_layer_change()

    #change labels layers ( 1 - 4 options in menu )
    def change_layers_of_labels_annotations(self, curent_label, change_layer_action):

        #create labes
        change_current_draw_rectangle = self.annotated_widget.draw_rectangle
        change_curent_label_id = curent_label["id"]

        #find current labels in list ( is e )
        for for_frame_annotations in change_current_draw_rectangle.fream_annotation.values():
            self.reorder_current_layer_in_frame(
                for_frame_annotations,
                lambda annotation: annotation.get("label_id") == change_curent_label_id,change_layer_action)

        # save ctrl + z history
        # redraw all
        self.finish_layer_change()

    #redraw all frame and save in ctr + z (end change in layers)
    def finish_layer_change(self):
        self.annotated_widget.draw_rectangle.on_annotion_comit()
        self.annotated_widget.update()

    #electe curent annotaion
    def delete_current_annotation(self, curent_annotation):

        #create new annotaion
        current_ddraw_rectangle = self.annotated_widget.draw_rectangle

        #find and delate current annotaion ( is equals and change value in list)
        for for_frame_annotations in current_ddraw_rectangle.fream_annotation.values():
            for_frame_annotations[:] = [annotation for annotation in for_frame_annotations if annotation is not curent_annotation]

        #if annotation is selected then unselect grab and edited mode
        edit_current_anotation = self.annotated_widget.edit_current_anotation
        if edit_current_anotation.select_current_annotation is curent_annotation:
            edit_current_anotation.deselecte_edited_mode()

        #save stage to ctrl z history
        current_ddraw_rectangle.on_annotion_comit()

        #refrash list of obciet right panel
        self.annotated_widget.update()
        self.refresh_all_objects_in_list()

    #delate all annotan of labels
    def delete_all_annotations_of_label(self, curent_label):

        #create new annotaion and label of id
        current_draw_rectangle = self.annotated_widget.draw_rectangle
        curent_label_id = curent_label["id"]

        #dealte all annotaion in current label (rest is stay)
        for for_frame_annotations in current_draw_rectangle.fream_annotation.values():
            for_frame_annotations[:] = [annotation for annotation in for_frame_annotations if annotation.get("label_id") != curent_label_id]

        #if annotation is selected then unselect grab and edited mode
        edit_current_anotation = self.annotated_widget.edit_current_anotation
        current_select_annotation = edit_current_anotation.select_current_annotation
        if current_select_annotation is not None and current_select_annotation.get("label_id") == curent_label_id:
            edit_current_anotation.deselecte_edited_mode()

        #save stage to ctrl z history
        current_draw_rectangle.on_annotion_comit()

        #refrash list of obciet right panel
        self.annotated_widget.update()
        self.refresh_all_objects_in_list()

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

        #create new QFrame (right row)
        annotation_row_widget = QFrame()

        #name of objeict style
        annotation_row_widget.setObjectName("annotation_row_frame")

        #set const fixed height of row
        annotation_row_widget.setFixedHeight(self.height_of_row)

        #set style of row widget
        annotation_row_widget.setStyleSheet(self.row_frame_style)
        #set laout
        annotation_row_layout = QHBoxLayout()

        #set left margin and spacing of layout
        annotation_row_layout.setContentsMargins(8, 2, 6, 2)
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
        visibility_annotation_button.setStyleSheet("QPushButton { border: none; background: transparent; }")

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
        locked_annotation_button.setStyleSheet("QPushButton { border: none; background: transparent; }")

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
        pinned_annotation_button.setStyleSheet("QPushButton { border: none; background: transparent; }")

        self.pin_icon_button(pinned_annotation_button, curent_annotation.get("pinned", False))

        #callback to pin fuction
        pinned_annotation_button.clicked.connect(
            lambda checked=False, current_annotation=curent_annotation, current_button=pinned_annotation_button:
            self.current_all_annotation_pin(current_annotation, current_button)
        )

        #add button to widget
        annotation_row_layout.addWidget(pinned_annotation_button)

       #4 button more option
       #deleate and layers change option
        more_action_button_menu = self.create_more_option_button(
            self.create_more_options_list(
                lambda layer_action, current_annotation=curent_annotation:
                    self.change_layers_of_annotations(current_annotation, layer_action),
                "Delete annotation",
                lambda current_annotation=curent_annotation: self.delete_current_annotation(current_annotation)))
        annotation_row_layout.addWidget(more_action_button_menu)

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
        current_button.setIcon(QIcon(self.visible_icon if is_visible else self.hidden_icon))
        current_button.setIconSize(QSize(self.size_of_icon, self.size_of_icon))

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
        current_button.setIcon(QIcon(self.locked_icon if is_locked else self.unlocked_icon))
        current_button.setIconSize(QSize(self.size_of_icon, self.size_of_icon))

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
        current_button.setIcon(QIcon(self.pinned_icon if is_pinned else self.unpinned_icon))
        current_button.setIconSize(QSize(self.size_of_icon, self.size_of_icon))

    # Refresh list of labes (if exist in list) and create annotaion option
    def refresh_all_labels_in_list(self):

        self.list_of_labels.clear()

        # current_labels
        for current_label in self.current_label_obiect.current_labels:

            #createn wighet for name and group option of label
            list_widget_item = QListWidgetItem()
            concurrent_row_widget = self.create_annotation_group_row_widget(current_label)
            list_widget_item.setSizeHint(concurrent_row_widget.sizeHint())

            #add to litems
            self.list_of_labels.addItem(list_widget_item)
            self.list_of_labels.setItemWidget(list_widget_item, concurrent_row_widget)

    #crate row for one label (group)
    def create_annotation_group_row_widget(self, curent_label):

        #create new widget (QFrame row)
        annotation_group_row_widget = QFrame()

        #name of objeict style
        annotation_group_row_widget.setObjectName("annotation_row_frame")

        #set const fixed height of row
        annotation_group_row_widget.setFixedHeight(self.height_of_row)

        #set style of row widget
        annotation_group_row_widget.setStyleSheet(self.row_frame_style)
        #set laout
        annotation_group_layout = QHBoxLayout()

        #set left margin and spacing of layout
        annotation_group_layout.setContentsMargins(8, 2, 6, 2)
        annotation_group_layout.setSpacing(4)
        #add layout to widged
        annotation_group_row_widget.setLayout(annotation_group_layout)

        #add to widget
        text_label = QLabel(curent_label["name"])
        annotation_group_layout.addWidget(text_label)

        #Stretch row
        annotation_group_layout.addStretch()

        #first button visibility of group (label)
        visibility_annotation_group_button = QPushButton()
        visibility_annotation_group_button.setFixedSize(self.size_of_icon, self.size_of_icon)
        visibility_annotation_group_button.setFlat(True)
        visibility_annotation_group_button.setStyleSheet("QPushButton { border: none; background: transparent; }")

        self.visibility_icon_button(visibility_annotation_group_button, curent_label.get("visible", True))

        #callback to group visibility fuction
        visibility_annotation_group_button.clicked.connect(
            lambda checked=False, current_label=curent_label, current_button=visibility_annotation_group_button:
            self.current_all_annotation_group_visibility(current_label, current_button)
        )

        #add button to widget
        annotation_group_layout.addWidget(visibility_annotation_group_button)

        #second button lock of group (label)
        locked_annotation_group_button = QPushButton()
        locked_annotation_group_button.setFixedSize(self.size_of_icon, self.size_of_icon)
        locked_annotation_group_button.setFlat(True)
        locked_annotation_group_button.setStyleSheet("QPushButton { border: none; background: transparent; }")

        self.lock_icon_button(locked_annotation_group_button, curent_label.get("locked", False))

        #callback to group lock fuction
        locked_annotation_group_button.clicked.connect(
            lambda checked=False, current_label=curent_label, current_button=locked_annotation_group_button:
            self.current_all_annotation_group_lock(current_label, current_button)
        )

        #add button to widget
        annotation_group_layout.addWidget(locked_annotation_group_button)

        #third button pin of group (label)
        pin_annotation_group_button = QPushButton()
        pin_annotation_group_button.setFixedSize(self.size_of_icon, self.size_of_icon)
        pin_annotation_group_button.setFlat(True)
        pin_annotation_group_button.setStyleSheet("QPushButton { border: none; background: transparent; }")

        self.pin_icon_button(pin_annotation_group_button, curent_label.get("pinned", False))

        #callback to group pin fuction
        pin_annotation_group_button.clicked.connect(
            lambda checked=False, current_label=curent_label, current_button=pin_annotation_group_button:
            self.current_all_annotation_group_pin(current_label, current_button)
        )

        #add button to widget
        annotation_group_layout.addWidget(pin_annotation_group_button)

        # 4 button more option
        # deleate and layers change option
        more_action_button_grupe_menu = self.create_more_option_button(
            self.create_more_options_list(
                lambda layer_action, current_label=curent_label:
                    self.change_layers_of_labels_annotations(current_label, layer_action),
                "Delete label",
                lambda current_label=curent_label: self.delete_all_annotations_of_label(current_label)))
        annotation_group_layout.addWidget(more_action_button_grupe_menu)

        return annotation_group_row_widget

    #redraw image and change visable flag
    def current_all_annotation_group_visibility(self, curent_annotation_group, button):

        #change flag of label
        curent_annotation_group["visible"] = not curent_annotation_group.get("visible", True)
        self.visibility_icon_button(button, curent_annotation_group["visible"])

        #apply to all annotations of this label
        self.annotated_widget.draw_rectangle.set_all_annotation_group_visible(curent_annotation_group["id"], curent_annotation_group["visible"])

        #redraw image
        self.annotated_widget.update()
        self.refresh_all_objects_in_list()

    # redraw image and change locked flag
    def current_all_annotation_group_lock(self, curent_annotation_group, button):

        #change flag of label
        curent_annotation_group["locked"] = not curent_annotation_group.get("locked", False)
        self.lock_icon_button(button, curent_annotation_group["locked"])

        #apply to all annotations of this label
        self.annotated_widget.draw_rectangle.set_all_annotation_group_locked(curent_annotation_group["id"], curent_annotation_group["locked"])

        #if current anntaion is selected then clear select and handers
        edit_current_anotation = self.annotated_widget.edit_current_anotation
        select_annotation = edit_current_anotation.select_current_annotation
        if select_annotation is not None and select_annotation.get("label_id") == curent_annotation_group["id"] and curent_annotation_group["locked"]:
            edit_current_anotation.deselecte_edited_mode()

        #redraw image
        self.annotated_widget.update()
        self.refresh_all_objects_in_list()


    #redraw image and change pinned flag
    def current_all_annotation_group_pin(self, curent_annotation_group, button):

        #change flag
        curent_annotation_group["pinned"] = not curent_annotation_group.get("pinned", False)
        self.pin_icon_button(button, curent_annotation_group["pinned"])

        #apply to all annotations of this label
        self.annotated_widget.draw_rectangle.set_all_annotation_group_pinned(curent_annotation_group["id"], curent_annotation_group["pinned"])

        #if is pin then stop move annotaion
        edit_current_anotation = self.annotated_widget.edit_current_anotation
        selected_annotation = edit_current_anotation.select_current_annotation
        if selected_annotation is not None and selected_annotation.get("label_id") == curent_annotation_group["id"] and curent_annotation_group["pinned"]:
            edit_current_anotation.if_pinned_then_cancel_move(selected_annotation)

        # redraw image
        self.annotated_widget.update()
        self.refresh_all_objects_in_list()