import csv
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class Load_labels_csv:

    #names of header
    header_names = ("name", "label", "labels", "class", "classes", "category", "label_name", "class_name")

    #utf-8-sig removes BOM from Excel
    encodings = ("utf-8-sig", "cp1250")

    #delimiters which are checked
    delimiters = (",", ";", "\t", "|")

    def __init__(self, load_labels_image_widget):

        #image widget (ButtonLogic)
        self.load_labels_image_widget = load_labels_image_widget

    #choose csv file and add all labels from it
    def load_labels_from_csv(self):

        #main window is parent of dialogs
        parent_window = self.load_labels_image_widget.window()

        csv_path, selected_filter = QFileDialog.getOpenFileName(
            parent_window, "Load labels from CSV", "", "CSV Files (*.csv);;All Files (*)")

        #user quit
        if not csv_path:
            return

        try:
            label_names = self.read_label_names(csv_path)
        except Exception as read_error:
            QMessageBox.critical(parent_window, "Load labels failed", str(read_error))
            return

        if not label_names:
            QMessageBox.warning(parent_window, "Load labels", "No labels found in the CSV file.")
            return

        new_labels_count, existing_labels_count = self.add_labels(label_names)

        QMessageBox.information(
            parent_window, "Load labels",
            f"New labels: {new_labels_count}\nAlready existing labels: {existing_labels_count}")

    #add labels to label log, return
    def add_labels(self, label_names):

        label_log = self.load_labels_image_widget.label_log

        new_labels_count = 0
        existing_labels_count = 0

        for label_name in label_names:

            labels_before = len(label_log.current_labels)
            #if label with this name exist then nothing is added
            label_log.add_label_to_list(label_name)

            if len(label_log.current_labels) > labels_before:
                new_labels_count += 1
            else:
                existing_labels_count += 1

        return new_labels_count, existing_labels_count

    #read file and return list of names
    def read_label_names(self, csv_path):

        with open(csv_path, "rb") as csv_file:
            file_bytes = csv_file.read()

        #try encodings one by one
        file_text = None
        for file_encoding in self.encodings:
            try:
                file_text = file_bytes.decode(file_encoding)
                break
            except UnicodeDecodeError:
                continue

        if file_text is None:
            raise ValueError("Cannot read the file (unknown encoding).")

        return self.parse_label_names(file_text)

    #names of labels from text of csv
    def parse_label_names(self, file_text):

        csv_rows = self.read_csv_rows(file_text)
        if not csv_rows:
            return []

        first_row = csv_rows[0]

        #header in first row: "name" / "label" / "class"
        name_column = None
        for column_index, cell_text in enumerate(first_row):
            if cell_text.lower() in self.header_names:
                name_column = column_index
                break

        raw_names = []
        if name_column is not None:
            raw_names = [row[name_column] for row in csv_rows[1:] if name_column < len(row)]
        elif len(csv_rows) == 1 and len(first_row) > 1:
            #one row without header: dog,cat,bird
            raw_names = first_row
        else:
            #no header: first column
            raw_names = [row[0] for row in csv_rows]

        #remove empty and duplicates
        label_names = []
        for raw_name in raw_names:
            label_name = raw_name.strip()
            if label_name and label_name not in label_names:
                label_names.append(label_name)

        return label_names

    #rows of csv without empty rows
    def read_csv_rows(self, file_text):

        text_lines = file_text.splitlines()

        #first not empty line is used to find the delimiter
        first_line = ""
        for text_line in text_lines:
            if text_line.strip():
                first_line = text_line
                break

        #the most frequent delimiter in first line
        file_delimiter = max(self.delimiters, key=first_line.count)

        csv_rows = []
        for csv_row in csv.reader(text_lines, delimiter=file_delimiter):
            stripped_row = [cell_text.strip() for cell_text in csv_row]
            if any(stripped_row):
                csv_rows.append(stripped_row)

        return csv_rows