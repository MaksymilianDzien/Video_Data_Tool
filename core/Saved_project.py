import os
import json


class Saved_project:

    def __init__(self, save_file_image_widget):

        #set image widget (connect  buttonLogic)
        self.save_file_image_widget = save_file_image_widget

    #save current porject to json file and save all iamge / video / frame
    def save_current_project_to_files(self, json_path_of_file):

        #try to save
        try:
            #crate draw rectangle and label log from image widget
            save_file_draw_rectangle = self.save_file_image_widget.draw_rectangle
            save_file_label_log = self.save_file_image_widget.label_log

            #extract the file name from current path
            current_output_folder_path = os.path.dirname(json_path_of_file)
            #extract the folder from current path
            current_file_name = os.path.splitext(os.path.basename(json_path_of_file))[0]

            #create folder for all image / video frames
            frames_output_folder = os.path.join(current_output_folder_path, f"{current_file_name}_files")
            os.makedirs(frames_output_folder, exist_ok=True)

            #data need to saved in jason
            #base iforamtaion to json
            project_jason_data = {
                #chek if is wideo (need from load)
                "is_video": self.save_file_image_widget.it_is_video,
                #all frame from video
                "frame_count": len(self.save_file_image_widget.All_frames),
                #name of labes
                "labels": self.build_data_of_labels(save_file_label_log),
                #current frames with annotaion
                "frames": {}
            }

            #save all load frames in program with annotaion and without annotaion
            for current_frame_index, current_frame_pixmap in enumerate(self.save_file_image_widget.All_frames):

                #craete name of file
                frame_image_file_name = f"frame_{current_frame_index}.png"
                #save current image(png change) with same name as current file
                current_frame_pixmap.save(os.path.join(frames_output_folder, frame_image_file_name), "PNG")

                #all annotation in current frame
                frame_annotations = save_file_draw_rectangle.fream_annotation.get(current_frame_index, [])

                #source file of orginal  frame
                source_file_name = ""
                if current_frame_index < len(self.save_file_image_widget.file_frame_name):
                    source_file_name = self.save_file_image_widget.file_frame_name[current_frame_index]

                #data of annotaion with file name
                project_jason_data["frames"][str(current_frame_index)] = {
                    "image_file": f"{current_file_name}_files/{frame_image_file_name}",
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