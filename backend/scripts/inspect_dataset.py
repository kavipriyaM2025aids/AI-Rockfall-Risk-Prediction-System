import os
import glob
import json
import hashlib
from collections import Counter
from PIL import Image

def inspect_dataset():
    dataset_path = r"C:\Users\kavi priya\Downloads\Open-Pit-Mine-Object-Detection-Dataset\Open-Pit-Mine-Object-Detection-Dataset"
    
    # Requirements
    images_dir = os.path.join(dataset_path, "images")
    annotations_dir = os.path.join(dataset_path, "annotation")
    
    # 1, 2
    image_files = glob.glob(os.path.join(images_dir, "**", "*.*"), recursive=True)
    image_files = [f for f in image_files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    json_files = glob.glob(os.path.join(annotations_dir, "**", "*.json"), recursive=True)
    
    # 6 Image formats
    image_formats = Counter([os.path.splitext(f)[1].lower() for f in image_files])
    
    # 18 Splits
    subdirs_images = set([os.path.basename(os.path.dirname(f)).lower() for f in image_files if os.path.basename(os.path.dirname(f)).lower() != 'images'])
    
    classes = Counter()
    objects_per_class = Counter()
    images_per_class = Counter()
    
    corrupt_jsons = []
    missing_fields_jsons = []
    non_rectangles = 0
    invalid_bboxes = 0
    outside_bboxes = 0
    zero_negative_bboxes = 0
    
    img_basenames = set([os.path.splitext(os.path.basename(f))[0] for f in image_files])
    ann_basenames = set([os.path.splitext(os.path.basename(f))[0] for f in json_files])
    
    # 8, 9
    images_without_annotations = img_basenames - ann_basenames
    annotations_without_images = ann_basenames - img_basenames
    
    for jf in json_files:
        try:
            with open(jf, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if 'shapes' not in data or 'imageWidth' not in data or 'imageHeight' not in data:
                missing_fields_jsons.append(jf)
                continue
                
            img_width = data['imageWidth']
            img_height = data['imageHeight']
            
            img_classes = set()
            for shape in data['shapes']:
                label = str(shape.get('label', 'unknown'))
                classes[label] += 1
                objects_per_class[label] += 1
                img_classes.add(label)
                
                shape_type = shape.get('shape_type')
                if shape_type != 'rectangle':
                    non_rectangles += 1
                
                points = shape.get('points', [])
                if len(points) == 2:
                    p1, p2 = points
                    x_min = min(p1[0], p2[0])
                    y_min = min(p1[1], p2[1])
                    x_max = max(p1[0], p2[0])
                    y_max = max(p1[1], p2[1])
                    
                    # 15
                    w = x_max - x_min
                    h = y_max - y_min
                    if w <= 0 or h <= 0:
                        zero_negative_bboxes += 1
                        invalid_bboxes += 1
                    # 14
                    elif x_min < 0 or y_min < 0 or x_max > img_width or y_max > img_height:
                        outside_bboxes += 1
                        invalid_bboxes += 1
                else:
                    invalid_bboxes += 1
                    
            for c in img_classes:
                images_per_class[c] += 1
                
        except Exception:
            corrupt_jsons.append(jf)
            
    # 7 Dimensions, 16 Duplicates, 17 Content duplicates
    image_dimensions = Counter()
    file_hashes = {}
    content_duplicates = 0
    duplicate_filenames = len(image_files) - len(set([os.path.basename(f) for f in image_files]))
    
    for img_path in image_files:
        try:
            with Image.open(img_path) as img:
                image_dimensions[img.size] += 1
        except Exception:
            pass
            
        # Optional: fast duplicate content check by file size + first few bytes
        try:
            sz = os.path.getsize(img_path)
            if sz in file_hashes:
                with open(img_path, 'rb') as f1, open(file_hashes[sz], 'rb') as f2:
                    if f1.read(1024) == f2.read(1024):
                        content_duplicates += 1
            else:
                file_hashes[sz] = img_path
        except:
            pass
            
    total_objects = sum(objects_per_class.values())
    class_imbalance = {k: f"{(v/total_objects)*100:.2f}%" for k, v in objects_per_class.items()} if total_objects > 0 else {}
    
    # 20 Look for metadata
    label_meanings = "No explicit meaning file found. Labels are numerical."
    for root, dirs, files in os.walk(dataset_path):
        for f in files:
            if 'class' in f.lower() or 'readme' in f.lower() or 'label' in f.lower():
                label_meanings += f" Found potential metadata: {f}."
                
    report = f'''DATASET INSPECTION REPORT
=========================

Dataset path:
{dataset_path}

Total images:
{len(image_files)}

Total JSON annotations:
{len(json_files)}

Image formats:
{dict(image_formats)}

Image dimensions:
{dict(image_dimensions)}

Unique classes:
{list(classes.keys())}

Objects per class:
{dict(objects_per_class)}

Images per class:
{dict(images_per_class)}

Images without annotations:
{len(images_without_annotations)}

Annotations without matching images:
{len(annotations_without_images)}

Invalid/corrupt JSON:
{len(corrupt_jsons)}

JSON files with missing required fields:
{len(missing_fields_jsons)}

Non-rectangle annotations:
{non_rectangles}

Invalid bounding boxes:
{invalid_bboxes} (Outside boundaries: {outside_bboxes}, Zero/negative dimensions: {zero_negative_bboxes})

Existing split:
{list(subdirs_images) if subdirs_images else "None"}

Class distribution:
{class_imbalance}

Potential duplicates:
Filenames: {duplicate_filenames}, Content: {content_duplicates}

Label meanings:
{label_meanings}
'''
    print(report)
    
    base_dir = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\backend"
    os.makedirs(base_dir, exist_ok=True)
    
    with open(os.path.join(base_dir, "dataset_inspection_report.txt"), "w", encoding='utf-8') as f:
        f.write(report)
        
    report_dict = {
        "dataset_path": dataset_path,
        "total_images": len(image_files),
        "total_json_annotations": len(json_files),
        "image_formats": dict(image_formats),
        "image_dimensions": {f"{k[0]}x{k[1]}": v for k, v in image_dimensions.items()},
        "unique_classes": list(classes.keys()),
        "objects_per_class": dict(objects_per_class),
        "images_per_class": dict(images_per_class),
        "images_without_annotations": len(images_without_annotations),
        "annotations_without_images": len(annotations_without_images),
        "corrupt_jsons": len(corrupt_jsons),
        "missing_fields_jsons": len(missing_fields_jsons),
        "non_rectangle_annotations": non_rectangles,
        "invalid_bboxes": invalid_bboxes,
        "outside_bboxes": outside_bboxes,
        "zero_negative_bboxes": zero_negative_bboxes,
        "existing_split": list(subdirs_images),
        "class_distribution": class_imbalance,
        "duplicate_filenames": duplicate_filenames,
        "content_duplicates": content_duplicates,
        "label_meanings": label_meanings
    }
    with open(os.path.join(base_dir, "dataset_inspection_report.json"), "w", encoding='utf-8') as f:
        json.dump(report_dict, f, indent=4)

if __name__ == "__main__":
    inspect_dataset()
