import json
import os
import re
import shutil
import tempfile
import zipfile
import xml.etree.ElementTree as ElementTree



class Import_annotation_formats:

    #YOLO auxiliary files
    yolo_files = ("obj.names", "obj.data", "classes.txt", "names.txt", "labels.txt", "train.txt", "val.txt", "test.txt")

    def __init__(self, import_image_file_widget):

        #import button logic widget with frames
        self.import_image_file_widget = import_image_file_widget

        #dictionaries for looking up a frame by filename
        self.frame_by_full_name = {}
        self.frame_by_stem = {}

    #COCO 1.0 .json
    def import_coco(self, cooc_json_path_file):

        try:
            #chek if frame are loaded
            coco_chek_error = self.check_frames_are_loaded()
            #if is error then just return in gui and False
            if coco_chek_error:
                return False, coco_chek_error

            #load json
            with open(cooc_json_path_file, "r", encoding="utf-8") as json_file:
                coco_data = json.load(json_file)

            #set return values from json file
            coco_parsed_frames, coco_label_names, coco_report = self.parse_coco(coco_data)
            #create annotation and return ture false
            return self.apply_parsed_frames(coco_parsed_frames, coco_label_names, coco_report)

        #if is error
        except Exception as import_error:
            #return in gui
            return False, str(import_error)

    #YOLO 1.1 / Ultralytics YOLO - folder or .zip
    def import_yolo(self, source_path):

        #set temp folder
        yolo_temp_folder = None
        try:
            # chek if frame are loaded
            yolo_chek_error = self.check_frames_are_loaded()
            # if is error then just return in gui and False
            if yolo_chek_error:
                return False, yolo_chek_error
            #retrun folder to load
            yolo_source_folder, yolo_temp_folder = self.prepare_source_folder(source_path)

            #parse YOLO file
            yolo_parsed_frames, yolo_label_names, yolo_report = self.parse_yolo(yolo_source_folder)
            # create annotation and return ture false
            return self.apply_parsed_frames(yolo_parsed_frames, yolo_label_names, yolo_report)
        # if is error
        except Exception as import_error:
            # return in gui
            return False, str(import_error)

        finally:
            #delete the temporary folder after unzipping the zip file
            if yolo_temp_folder:
                shutil.rmtree(yolo_temp_folder, ignore_errors=True)

    #PASCAL VOC 1.1 - folder or .zip (.xml)
    def import_pascal_voc(self, source_path):
        # set temp folder
        voc_temp_folder = None
        try:
            # chek if frame are loaded
            voc_chek_error = self.check_frames_are_loaded()
            # if is error then just return in gui and False
            if voc_chek_error:
                return False, voc_chek_error
            # retrun folder to load
            voc_source_folder, voc_temp_folder = self.prepare_source_folder(source_path)
            # parse VOC file
            voc_parsed_frames, voc_label_names, voc_report = self.parse_pascal_voc(voc_source_folder)
            # create annotation and return ture false
            return self.apply_parsed_frames(voc_parsed_frames, voc_label_names, voc_report)
        # if is error
        except Exception as import_error:
            # return in gui
            return False, str(import_error)

        finally:
            # delete the temporary folder after unzipping the zip file
            if voc_temp_folder:
                shutil.rmtree(voc_temp_folder, ignore_errors=True)

    #COCO: images + annotations + categories
    def parse_coco(self, coco_data):

        #categories: id -> name
        category_names = {}
        label_names = []
        #load  categories and set in label names
        for category in coco_data.get("categories", []):
            category_names[category["id"]] = category["name"]
            label_names.append(category["name"])

        #images: id -> image data
        coco_images = {coco_image["id"]: coco_image for coco_image in coco_data.get("images", [])}

        #number of frame
        parsed_frames = {}
        #number for skipped items
        report = self.new_report()

        #loop through all annotations from the file
        for coco_annotation in coco_data.get("annotations", []):

            #find image for this annotation from image_id
            coco_image = coco_images.get(coco_annotation.get("image_id"))
            #if is none then skip and add one to report
            if coco_image is None:
                report["skipped"] += 1
                continue
            #image filename from COCO
            file_name = coco_image.get("file_name", "")
            #find the frame number from the file name
            frame_index = self.find_frame_index(file_name)
            #if not found frame
            if frame_index is None:
                #Add the name to the collection and move to the next annotation.
                report["unmatched_files"].add(os.path.basename(str(file_name)))
                continue

            #scale if the size in the file differs from the loaded frame
            frame_width, frame_height = self.get_frame_size(frame_index)
            scale_x = frame_width / coco_image["width"] if coco_image.get("width") else 1.0
            scale_y = frame_height / coco_image["height"] if coco_image.get("height") else 1.0

            #category of id annotation
            category_id = coco_annotation.get("category_id")
            #name of category
            label_name = category_names.get(category_id, f"category_{category_id}")
            #if this name is not on the list of labels, add it.
            if label_name not in label_names:
                label_names.append(label_name)

            shapes = []

            #poligony
            segmentation = coco_annotation.get("segmentation")
            if isinstance(segmentation, list):
                for flat_points in segmentation:
                    if isinstance(flat_points, list) and len(flat_points) >= 6:
                        points = [{"x": float(flat_points[i]) * scale_x, "y": float(flat_points[i + 1]) * scale_y}
                                  for i in range(0, len(flat_points) - 1, 2)]
                        shapes.append({"type": "polygon", "points": points})

            #RLE dictionary mask is not supported  just count
            elif isinstance(segmentation, dict):
                report["masks_as_box"] += 1

            #rectangle with bbox
            if not shapes:
                bbox = coco_annotation.get("bbox")
                if bbox and len(bbox) == 4 and bbox[2] > 0 and bbox[3] > 0:
                    shapes.append({"type": "rectangle",
                                   "x": float(bbox[0]) * scale_x, "y": float(bbox[1]) * scale_y,
                                   "width": float(bbox[2]) * scale_x, "height": float(bbox[3]) * scale_y})
                else:
                    report["skipped"] += 1

            #Assign a label name to each shape and add it to its frame
            for shape in shapes:
                shape["label_name"] = label_name
                parsed_frames.setdefault(frame_index, []).append(shape)

        return parsed_frames, label_names, report

    #YOLO: file .txt,
    def parse_yolo(self, source_folder):

        # class names by number and list of labels
        class_names = self.read_yolo_class_names(source_folder)
        label_names = list(class_names)
        parsed_frames = {}
        report = self.new_report()

        #go through the folder and all subfolders
        for folder_path, folder_names, file_names in os.walk(source_folder):
            #go through all files
            for file_name in file_names:

                if not file_name.lower().endswith(".txt"):
                    continue
                if file_name.lower() in self.yolo_files:
                    continue

                #find a frame by name
                frame_index = self.find_frame_index(file_name)
                if frame_index is None:
                    report["unmatched_files"].add(file_name)
                    continue

                #size of frame in px
                frame_width, frame_height = self.get_frame_size(frame_index)

                #open txt files
                with open(os.path.join(folder_path, file_name), "r", encoding="utf-8", errors="ignore") as txt_file:
                    #one line one object
                    for line in txt_file:
                        line_parts = line.split()
                        #less than 5 items skip
                        if len(line_parts) < 5:
                            continue

                        try:
                            class_id = int(float(line_parts[0]))
                            values = [float(value) for value in line_parts[1:]]
                        #it cannot be exchanged
                        except ValueError:
                            report["skipped"] += 1
                            continue

                        #class name from a file containing names
                        if 0 <= class_id < len(class_names):
                            label_name = class_names[class_id]
                        else:
                            label_name = f"class_{class_id}"
                            #If it is not on the list of labels, add it
                            if label_name not in label_names:
                                label_names.append(label_name)

                        #rectangle: cx cy w h
                        if len(values) in (4, 5):
                            center_x, center_y, box_width, box_height = values[:4]
                            shape = {"type": "rectangle",
                                     "x": (center_x - box_width / 2) * frame_width,
                                     "y": (center_y - box_height / 2) * frame_height,
                                     "width": box_width * frame_width,
                                     "height": box_height * frame_height}

                        #polygon: x1 y1 x2 y2
                        elif len(values) >= 6 and len(values) % 2 == 0:
                            points = [{"x": values[i] * frame_width, "y": values[i + 1] * frame_height}
                                      for i in range(0, len(values), 2)]
                            shape = {"type": "polygon", "points": points}

                        #rest is not supported
                        else:
                            report["skipped"] += 1
                            continue
                        #add a label
                        shape["label_name"] = label_name
                        #add a shape to the frame
                        parsed_frames.setdefault(frame_index, []).append(shape)

        return parsed_frames, label_names, report

    #PASCAL VOC: files .xml
    def parse_pascal_voc(self, source_folder):

        parsed_frames = {}
        #list of labels
        label_names = []
        report = self.new_report()

        #go through the folder and all subfolders
        for folder_path, folder_names, file_names in os.walk(source_folder):
            #go through all files
            for file_name in file_names:

                #only .xml
                if not file_name.lower().endswith(".xml"):
                    continue

                #load the XML and retrieve the root element
                try:
                    xml_root = ElementTree.parse(os.path.join(folder_path, file_name)).getroot()
                except ElementTree.ParseError:
                    report["skipped"] += 1
                    continue

                #is not voc file
                if xml_root.tag != "annotation":
                    continue

                #first the name from <filename>, then the XML filename
                frame_index = self.find_frame_index(xml_root.findtext("filename") or "")
                if frame_index is None:
                    frame_index = self.find_frame_index(file_name)
                if frame_index is None:
                    report["unmatched_files"].add(file_name)
                    continue

                #scaling if the size in the XML differs from the loaded frame
                frame_width, frame_height = self.get_frame_size(frame_index)
                scale_x = scale_y = 1.0
                size_element = xml_root.find("size")
                #if it exists
                if size_element is not None:
                    try:
                        file_width = float(size_element.findtext("width"))
                        file_height = float(size_element.findtext("height"))
                        if file_width > 0 and file_height > 0:
                            scale_x = frame_width / file_width
                            scale_y = frame_height / file_height
                    except (TypeError, ValueError):
                        pass

                #each <object> is one frame
                for object_element in xml_root.findall("object"):

                    #<bndbox> element with coordinates
                    bndbox = object_element.find("bndbox")
                    if bndbox is None:
                        report["skipped"] += 1
                        continue
                    #load xmin, ymin, xmax, ymax as numbers
                    try:
                        x_min = float(bndbox.findtext("xmin"))
                        y_min = float(bndbox.findtext("ymin"))
                        x_max = float(bndbox.findtext("xmax"))
                        y_max = float(bndbox.findtext("ymax"))
                    except (TypeError, ValueError):
                        report["skipped"] += 1
                        continue
                    #inverted or zero frame
                    if x_max <= x_min or y_max <= y_min:
                        report["skipped"] += 1
                        continue
                    #class name from <name>, defaulting to 'object'
                    label_name = (object_element.findtext("name") or "object").strip()
                    if label_name not in label_names:
                        label_names.append(label_name)
                    #add a rectangle to the frame; width = xmax - xmin; multiply everything by the scale
                    parsed_frames.setdefault(frame_index, []).append(
                        {"type": "rectangle", "label_name": label_name,
                         "x": x_min * scale_x, "y": y_min * scale_y,
                         "width": (x_max - x_min) * scale_x, "height": (y_max - y_min) * scale_y})

        return parsed_frames, label_names, report

    #import report
    def new_report(self):
        return {"unmatched_files": set(), "skipped": 0, "masks_as_box": 0}

    #check if the frames have been loaded and prepare the name dictionaries
    def check_frames_are_loaded(self):

        image_widget = self.import_image_file_widget

        if not image_widget.All_frames:
            return "Load images or video first, then import annotations."

        self.frame_by_full_name = {}
        self.frame_by_stem = {}

        for frame_index, frame_name in enumerate(image_widget.file_frame_name):
            self.frame_by_full_name.setdefault(frame_name.lower(), frame_index)
            self.frame_by_stem.setdefault(os.path.splitext(frame_name)[0].lower(), frame_index)

        return None

    #size of the loaded frame in pixels
    def get_frame_size(self, frame_index):
        frame_pixmap = self.import_image_file_widget.All_frames[frame_index]
        return frame_pixmap.width(), frame_pixmap.height()

    #find the frame index by filename
    def find_frame_index(self, file_name):

        #base name of file
        base_name = os.path.basename(str(file_name).replace("\\", "/"))
        if not base_name:
            return None

        #name without extension, in lowercase letters
        file_stem = os.path.splitext(base_name)[0].lower()
        #iamge widget
        image_widget = self.import_image_file_widget

        #video: frame-type names 000012
        if image_widget.it_is_video:
            frame_numbers = re.findall(r"\d+", file_stem)
            if not frame_numbers:
                return None
            frame_index = int(frame_numbers[-1])
            if 0 <= frame_index < len(image_widget.All_frames):
                return frame_index
            return None

        #images full name  then the name alone without the extension
        if base_name.lower() in self.frame_by_full_name:
            return self.frame_by_full_name[base_name.lower()]
        return self.frame_by_stem.get(file_stem)

    #prepare folder or zip
    def prepare_source_folder(self, source_path):

        #if is in folder
        if os.path.isdir(source_path):
            return source_path, None
        #not folder not zip
        if not zipfile.is_zipfile(source_path):
            raise ValueError("Select a folder or a .zip file.")

        #create an empty temporary folder
        temp_folder = tempfile.mkdtemp(prefix="annotations_import_")
        #full path to the temporary folder
        real_temp_folder = os.path.realpath(temp_folder)

        #open the zip file for reading
        with zipfile.ZipFile(source_path, "r") as zip_file:
            for member_name in zip_file.namelist():
                #do not unpack outside the temporary folder
                member_path = os.path.realpath(os.path.join(temp_folder, member_name))
                if not member_path.startswith(real_temp_folder):
                    shutil.rmtree(temp_folder, ignore_errors=True)
                    raise ValueError("Unsafe path inside zip file.")
            #unpack everything
            zip_file.extractall(temp_folder)
        #return 2 folder
        return temp_folder, temp_folder

    #read class names  YOLO: obj.names / classes.txt / names.txt / data.yaml
    def read_yolo_class_names(self, source_folder):

        #first file found containing names
        found_names_files = {}
        #all found YAML files
        found_yaml_files = []

        #go through the entire folder
        for folder_path, folder_names, file_names in os.walk(source_folder):
            for file_name in file_names:
                lower_name = file_name.lower()
                if lower_name in ("obj.names", "classes.txt", "names.txt") and lower_name not in found_names_files:
                    found_names_files[lower_name] = os.path.join(folder_path, file_name)
                elif lower_name.endswith((".yaml", ".yml")):
                    found_yaml_files.append(os.path.join(folder_path, file_name))

        #list from a text file
        for names_file_name in ("obj.names", "classes.txt", "names.txt"):
            if names_file_name in found_names_files:
                with open(found_names_files[names_file_name], "r", encoding="utf-8", errors="ignore") as names_file:
                    return [line.strip() for line in names_file if line.strip()]

        #data.yaml
        for yaml_path in found_yaml_files:
            with open(yaml_path, "r", encoding="utf-8", errors="ignore") as yaml_file:
                yaml_names = self.read_names_from_yaml_text(yaml_file.read())
            if yaml_names:
                return yaml_names

        return []

    #paser yaml
    def read_names_from_yaml_text(self, yaml_text):

        #YAML text as a list of lines
        yaml_lines = yaml_text.splitlines()
        #every line with a number
        for line_index, line in enumerate(yaml_lines):
            #looking for a line that starts with 'names:'
            if not line.startswith("names:"):
                continue

            rest_of_line = line[len("names:"):].strip()

            #it starts with [a, b, c]
            if rest_of_line.startswith("["):
                inside_brackets = rest_of_line.strip("[]")
                return [name.strip().strip("'\"") for name in inside_brackets.split(",") if name.strip()]

            #number -> name dictionary
            names_by_id = {}
            names_list = []
            #subsequent lines after 'names:'
            for next_line in yaml_lines[line_index + 1:]:

                if not next_line.strip():
                    continue
                if not next_line.startswith((" ", "\t", "-")):
                    break
                #line with no spaces at the edges
                stripped_line = next_line.strip()
                if stripped_line.startswith("- "):
                    names_list.append(stripped_line[2:].strip().strip("'\""))
                elif ":" in stripped_line:
                    key_text, value_text = stripped_line.split(":", 1)
                    if key_text.strip().isdigit():
                        names_by_id[int(key_text.strip())] = value_text.strip().strip("'\"")

            #sequence with numbers: a list of numbers in order, with missing numbers represented as class_i
            if names_by_id:
                return [names_by_id.get(i, f"class_{i}") for i in range(max(names_by_id) + 1)]
            return names_list

        return []

    #insert the incorporated annotations into the program
    def apply_parsed_frames(self, parsed_frames, label_names, report):

        #nothing fits
        total_annotations = sum(len(frame_shapes) for frame_shapes in parsed_frames.values())
        if total_annotations == 0:
            unmatched_text = ""
            if report["unmatched_files"]:
                unmatched_text = " Files without matching frame: " + ", ".join(sorted(report["unmatched_files"])[:5])
            return False, "No annotations matched the loaded frames." + unmatched_text

        #set image rectangle and label log
        image_widget = self.import_image_file_widget
        draw_rectangle = image_widget.draw_rectangle
        label_log = image_widget.label_log

        #new labels
        label_log.current_labels = []
        label_log.label_next_id = 1

        label_id_by_name = {}
        #for each name from the list
        for label_name in label_names:
            #only if that name doesn't exist yet
            if label_name not in label_id_by_name:
                label_id_by_name[label_name] = self.create_label(label_log, label_name)

        #new labels
        new_frame_annotations = {}
        next_annotation_id = 1

        #frames one by one
        for frame_index in sorted(parsed_frames):
            #single-frame annotations
            one_frame_annotations = []

            #every shape of this cage
            for shape in parsed_frames[frame_index]:

                new_annotation = {
                    "id": next_annotation_id,
                    "type": shape["type"],
                    "label_id": label_id_by_name.get(shape["label_name"]),
                    "rotation": 0.0,
                    "layer": 1,
                    "visible": True,
                    "locked": False,
                    "pinned": False,
                }

                if shape["type"] == "polygon":
                    new_annotation["points"] = [{"x": round(point["x"], 2), "y": round(point["y"], 2)}
                                                for point in shape["points"]]
                else:
                    new_annotation["x"] = round(shape["x"], 2)
                    new_annotation["y"] = round(shape["y"], 2)
                    new_annotation["width"] = round(shape["width"], 2)
                    new_annotation["height"] = round(shape["height"], 2)

                #add annotations to the frame
                one_frame_annotations.append(new_annotation)
                #next id
                next_annotation_id += 1

            #save the annotations for this frame
            new_frame_annotations[frame_index] = one_frame_annotations

        draw_rectangle.fream_annotation = new_frame_annotations
        draw_rectangle.next_annotation_id = next_annotation_id

        #deselect edited annotations
        image_widget.edit_current_anotation.deselecte_edited_mode()

        #refresh the right panel
        draw_rectangle.current_annotations_changed()
        if label_log.on_labels_changed:
            label_log.on_labels_changed()
        image_widget.update()

        #if success and summary text
        return True, self.build_summary(total_annotations, len(new_frame_annotations), len(label_id_by_name), report)

    #create label
    def create_label(self, label_log, label_name):

        ids_before = {label["id"] for label in label_log.current_labels}
        new_label_id = label_log.add_label_to_list(label_name)

        if isinstance(new_label_id, int):
            return new_label_id

        #if add_label_to_list returned nothing
        for label in label_log.current_labels:
            if label["id"] not in ids_before:
                return label["id"]

        return None

    #summary text for the user
    def build_summary(self, annotation_count, frame_count, label_count, report):

        summary_lines = [f"Imported {annotation_count} annotations in {frame_count} frames, {label_count} labels."]

        if report["unmatched_files"]:
            summary_lines.append(f"{len(report['unmatched_files'])} file(s) had no matching frame and were skipped.")
        if report["skipped"]:
            summary_lines.append(f"{report['skipped']} unsupported or invalid item(s) were skipped.")
        if report["masks_as_box"]:
            summary_lines.append(f"{report['masks_as_box']} mask(s) were imported as rectangles.")

        return "\n".join(summary_lines)