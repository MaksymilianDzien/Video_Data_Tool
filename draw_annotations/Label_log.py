from PyQt5.QtWidgets import QInputDialog


class Label_log:

    # str
    default_label_option = "* Create new Label"

    def __init__(self):
        #set all labels
        self.current_labels = []

    # add label to menu if exist
    def add_label_to_list(self, current_name_of_label):
        #chek if exist
        if current_name_of_label and current_name_of_label not in self.current_labels:
            self.current_labels.append(current_name_of_label)

    # select label options  fuction 
    def choose_annotation_label_option(self, current_widgets):

        # create new list to chose of labes (if is not set oprtion to create
        new_labels_option = self.current_labels + [self.default_label_option]

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

            #add new label to list
            self.add_label_to_list(new_label_name)
            return new_label_name, True

        # if exist select that option
        return select_chosen_option, True