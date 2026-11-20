import json


class Saved_project:

    def __init__(self, save_file_image_widget):

        #set image widget (connect  buttonLogic)
        self.save_file_image_widget = save_file_image_widget


    #save current project to json file
    def save_current_project_to_files(self, json_path_of_file):

        #try to save
        try:
            #crate draw rectangle and label log from image widget
            save_file_draw_rectangle = self.save_file_image_widget.draw_rectangle
            save_file_label_log = self.save_file_image_widget.label_log

            #base iforamtaion to json
            project_jason_data = {
                #chek if is wideo
                "is_video": self.save_file_image_widget.it_is_video,
                #all frame count
                "frame_count": len(self.save_file_image_widget.All_frames),
                #next ids of annotations
                "next_annotation_id": save_file_draw_rectangle.next_annotation_id,
                "next_label_id": save_file_label_log.label_next_id,
                #name of labes
                "labels": self.build_data_of_labels(save_file_label_log),
                #only frames with annotaion
                "frames": {}
            }

            #save only frames witch have annotaion
            for current_frame_index, frame_annotations in save_file_draw_rectangle.fream_annotation.items():

                #if frame without annotaion then skip
                if not frame_annotations:
                    continue

                #source file of orginal  frame
                source_file_name = ""
                if current_frame_index < len(self.save_file_image_widget.file_frame_name):
                    source_file_name = self.save_file_image_widget.file_frame_name[current_frame_index]

                #data of annotaion with index of frame
                project_jason_data["frames"][str(current_frame_index)] = {
                    "source_file_name": source_file_name,
                    "annotations": [dict(annotation) for annotation in frame_annotations]
                }

            #save in json file with user pint name
            with open(json_path_of_file, "w", encoding="utf-8") as json_file:
                json.dump(project_jason_data, json_file, indent=2)

            return True, None

        #catch for pint int gui if not work
        except Exception as save_error:
            return False, str(save_error)

    #bulit list of label to save
    def build_data_of_labels(self, label_log):
        return [dict(label) for label in label_log.current_labels]