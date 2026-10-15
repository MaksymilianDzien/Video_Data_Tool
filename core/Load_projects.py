import json


class Load_projects:

    #chek  file names
    check_names_files = True

    def __init__(self, load_image_file_widget):

        #set image widget
        self.load_image_file_widget = load_image_file_widget

    #load annotation poreocjet form file
    def load_current_project_from_file(self, json_path_file):

        #try to open
        try:
            #read json file
            with open(json_path_file, "r", encoding="utf-8") as json_file:
                project_json_all_data = json.load(json_file)

            #set wiget ,rectangle , labellog
            image_widget = self.load_image_file_widget
            draw_rectangle = image_widget.draw_rectangle
            label_log = image_widget.label_log

            #iamges / or vide must be load first
            if not image_widget.All_frames:
                return False, "Load images or video first, then load the project."

            #chek if is video or images
            if project_json_all_data.get("is_video") != image_widget.it_is_video:
                return False, "Project was saved for different type of file video or images."

            #chek if is the same number of frames
            if project_json_all_data.get("frame_count") != len(image_widget.All_frames):
                return False, (
                    f"Project has {project_json_all_data.get('frame_count')} frames, "
                    f"but {len(image_widget.All_frames)} frames are loaded."
                )

            #chek and set labels
            file_labels = []
            file_label_ids = set()

            #loop for get all lables from file
            for saved_labels in project_json_all_data.get("labels", []):

                #chcek if id is in file
                if "id" not in saved_labels or "name" not in saved_labels:
                    return False, "Label without id or name in project file."

                #create label and set left panel option
                file_label = dict(saved_labels)
                file_label.setdefault("visible", True)
                file_label.setdefault("locked", False)
                file_label.setdefault("pinned", False)

                #add label witch id
                file_labels.append(file_label)
                file_label_ids.add(file_label["id"])

            #set list from anotaion
            file_frame_annotations = {}

            #loop for all adontation
            for file_frame_key, file_frame_data in project_json_all_data.get("frames", {}).items():

                file_frame_index = int(file_frame_key)

                #chek if index of frame is out of range
                if not 0 <= file_frame_index < len(image_widget.All_frames):
                    return False, f"Frame {file_frame_index + 1} does not exist in loaded files."

                #chek if name of file is the same as in saved project
                if self.check_names_files:
                    saved_file_name = file_frame_data.get("source_file_name", "")

                    current_file_name = ""
                    if file_frame_index < len(image_widget.file_frame_name):
                        current_file_name = image_widget.file_frame_name[file_frame_index]

                    if saved_file_name and saved_file_name != current_file_name:
                        return False, (
                            f"Frame {file_frame_index + 1}: project was saved for file "
                            f"'{saved_file_name}', but '{current_file_name}' is loaded."
                        )
                #set table of annotaion
                file_frame_annotations = []
                #loop for saved annotaion
                for saved_annotation in file_frame_data.get("annotations", []):

                    #chcek if is error
                    annotation_error = self.chek_file_annotation(saved_annotation, file_label_ids)
                    if annotation_error:
                        return False, f"Frame {file_frame_index + 1}: {annotation_error}"

                    #create new annotaion form file optin right panel
                    file_new_annotation = dict(saved_annotation)
                    file_new_annotation.setdefault("layer", 1)
                    file_new_annotation.setdefault("visible", True)
                    file_new_annotation.setdefault("locked", False)
                    file_new_annotation.setdefault("pinned", False)

                    #add to table
                    file_frame_annotations.append(file_new_annotation)

                if file_frame_annotations:
                    file_frame_annotations[file_frame_index] = file_frame_annotations

            #next ids  never smaller than used id
            used_annotation_ids = [annotation["id"]
                for frame_annotations in file_frame_annotations.values()
                for annotation in frame_annotations]

            used_label_ids = [label["id"] for label in file_labels]

            next_annotation_id = project_json_all_data.get("next_annotation_id", 1)
            if used_annotation_ids:
                next_annotation_id = max(next_annotation_id, max(used_annotation_ids) + 1)

            next_label_id = project_json_all_data.get("next_label_id", 1)
            if used_label_ids:
                next_label_id = max(next_label_id, max(used_label_ids) + 1)

            #change current state of program
            label_log.current_labels = file_labels
            label_log.label_next_id = next_label_id

            draw_rectangle.fream_annotation = file_frame_annotations
            draw_rectangle.next_annotation_id = next_annotation_id

            #clear selected annotation
            image_widget.edit_current_anotation.deselecte_edited_mode()

            #refresh right panel
            draw_rectangle.current_annotations_changed()
            if label_log.on_labels_changed:
                label_log.on_labels_changed()
            image_widget.update()

            return True, None

        #catch for pint in gui if not work
        except Exception as load_error:
            return False, str(load_error)

    #chek one annotation
    def chek_file_annotation(self, file_annotation, file_label_ids):

        #base keys of every annotation
        for key in ("id", "type", "label_id", "rotation"):
            if key not in file_annotation:
                return f"annotation without '{key}'."

        #label of annotation must exist in labels
        if file_annotation["label_id"] is not None and file_annotation["label_id"] not in file_label_ids:
            return f"annotation {file_annotation['id']} has unknown label."

        #polygon have list of points, rectangle and oval have x, y, width, height
        if file_annotation["type"] == "polygon":

            points = file_annotation.get("points")
            if not isinstance(points, list) or len(points) < 3:
                return f"polygon {file_annotation['id']} has bad points."

            for point in points:
                if "x" not in point or "y" not in point:
                    return f"polygon {file_annotation['id']} has bad points."

        elif file_annotation["type"] in ("rectangle", "oval"):

            for key in ("x", "y", "width", "height"):
                if key not in file_annotation:
                    return f"annotation {file_annotation['id']} without '{key}'."

        else:
            return f"annotation {file_annotation['id']} has unknown type '{file_annotation['type']}'."

        return None