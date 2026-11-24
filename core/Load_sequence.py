import os
import re

class Load_sequence:

    #file ext
    file_extensions = (".png", ".jpg", ".jpeg", ".bmp")

    def __init__(self, load_main_window):

        #set main window
        self.load_main_window = load_main_window

    #load sequence from one file
    def load_sequence(self, selected_image_path):


        try:

            load_sequence_paths = self.find_sequence_paths(selected_image_path)
            # if sequence path is empty
            if not load_sequence_paths:
                return False, "Selected file is not a supported image."

            #load file like find file
            self.load_main_window.load_image_to_gui(load_sequence_paths)

            #set slider from file name
            selected_index = self.find_selected_index(load_sequence_paths, selected_image_path)
            if selected_index > 0:
                self.load_main_window.frame_slider.setValue(selected_index + 1)

            #retrun len of load images
            return True, f"Loaded {len(load_sequence_paths)} images."

        #if error
        except Exception as sequence_error:
            #print error
            return False, str(sequence_error)

    #
    def find_sequence_paths(self, selected_image_path):

        #change in abspath
        selected_image_path = os.path.abspath(selected_image_path)
        #same folder
        folder_path = os.path.dirname(selected_image_path)
        #same ext
        selected_file_name = os.path.basename(selected_image_path)

        #split file to name and .ext
        selected_stem, selected_extension = os.path.splitext(selected_file_name)

        #bad ext name
        if selected_extension.lower() not in self.file_extensions:
            return []

        #split name and number  a 1
        selected_prefix, selected_number = self.split_name_and_number(selected_stem)
        if selected_number is None:
            return [selected_image_path]

        #empty list
        sequence_items = []
        #loop for all file in folder
        for file_name in os.listdir(folder_path):

            #split file  name . ext
            stem, extension = os.path.splitext(file_name)
            if extension.lower() != selected_extension.lower():
                continue

            #split name and number
            prefix, number = self.split_name_and_number(stem)
            if number is None or prefix.lower() != selected_prefix.lower():
                continue

            #add to list number , file name
            sequence_items.append((number, file_name))

        #sort list
        sequence_items.sort()

        #retrun path list
        return [os.path.join(folder_path, file_name) for number, file_name in sequence_items]

    #splits the name into a beginning part and a number
    def split_name_and_number(self, file_stem):

        match = re.match(r"^(.*?)(\d+)$", file_stem)
        if match is None:
            return file_stem, None

        return match.group(1), int(match.group(2))

    #index of the specified image in the sequence list
    def find_selected_index(self, sequence_paths, selected_image_path):

        #normcase path
        selected_image_path = os.path.normcase(os.path.abspath(selected_image_path))
        #loop for all index of path list and normcase
        for index, sequence_path in enumerate(sequence_paths):
            if os.path.normcase(os.path.abspath(sequence_path)) == selected_image_path:
                return index
        #retrun first frame
        return 0