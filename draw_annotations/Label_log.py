from PyQt5.QtWidgets import QInputDialog


class Label_log:

    # str
    default_label_option = "* Create new Label"

    def __init__(self):

        #set all labels
        self.current_labels = []

        # set start id
        self.label_next_id = 1

        # callback new label (if exist)
        self.on_labels_changed = None

    # add label to menu if exist
    def add_label_to_list(self, current_name_of_label):

        if not current_name_of_label:
            return None

        #  chek if exist retrun id of label
        for existing_label in self.current_labels:
            if existing_label["name"] == current_name_of_label:
                return existing_label["id"]

        #create new and +1 to next label
        new_label = {"id": self.label_next_id, "name": current_name_of_label}
        self.current_labels.append(new_label)
        self.label_next_id += 1

        # callback right panel abaut new lable
        if self.on_labels_changed:
            self.on_labels_changed()

        return new_label["id"]

    # get label name of label from id
    def get_label_name(self, current_label_id):

        #retrun name from id
        for label in self.current_labels:
            if label["id"] == current_label_id:
                return label["name"]

        #
        return ""

    # select label options fuction
    def choose_annotation_label_option(self, current_widgets):

        # create new list to chose of labes (if is not set oprtion to create
        label_names = [label["name"] for label in self.current_labels]
        new_labels_option = label_names + [self.default_label_option]

        #select option in label menu
        select_chosen_option, ok = (
            QInputDialog.getItem
                (
            current_widgets, "Select label", "Label:", new_labels_option, 0, False
                ))

        #not select just exit
        if not ok:
            return None, False

        # create new label
        if select_chosen_option == self.default_label_option:
            new_label_name, ok_second = (QInputDialog.getText
                (
                current_widgets, "New label", "Set name to label:"
                ))

            #if not select just claine
            if not ok_second or not new_label_name:
                return None, False

            #add new label to list  retrun current label id
            new_label_id = self.add_label_to_list(new_label_name)
            return new_label_id, True

        # if exist select that option from id to name if is selected that option
        for label in self.current_labels:
            if label["name"] == select_chosen_option:
                return label["id"], True

        return None, False