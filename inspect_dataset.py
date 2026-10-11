import os
import glob
import json
import xml.etree.ElementTree as ET
from PIL import Image

def inspect():
    dataset_path = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\dataset\Open-Pit-Mine-Object-Detection-Dataset\Open-Pit-Mine-Object-Detection-Dataset"
    
    images_dir = os.path.join(dataset_path, "images")
    annotations_dir = os.path.join(dataset_path, "annotation")
    
    image_files = glob.glob(os.path.join(images_dir, "**", "*.*"), recursive=True)
    annotation_files = glob.glob(os.path.join(annotations_dir, "**", "*.*"), recursive=True)
    
    image_formats = set()
    image_dimensions = set()
    valid_images = []
    
    print(f"Total image files found: {len(image_files)}")
    print(f"Total annotation files found: {len(annotation_files)}")
    
    for img_path in image_files:
        ext = os.path.splitext(img_path)[1].lower()
        image_formats.add(ext)
        if ext in ['.jpg', '.jpeg', '.png']:
            try:
                with Image.open(img_path) as img:
                    image_dimensions.add(img.size)
                    valid_images.append(img_path)
            except Exception as e:
                print(f"Corrupted image: {img_path}")
                
    print(f"Image formats: {list(image_formats)}")
    print(f"Sample image dimensions: {list(image_dimensions)[:5]}")
    
    # Check annotation format and classes
    annotation_formats = set([os.path.splitext(f)[1].lower() for f in annotation_files])
    print(f"Annotation formats: {list(annotation_formats)}")
    
    classes = {}
    total_objects = 0
    missing_annotations = 0
    
    if '.xml' in annotation_formats:
        for xml_file in annotation_files:
            if not xml_file.endswith('.xml'): continue
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                for obj in root.findall('object'):
                    name = obj.find('name').text
                    classes[name] = classes.get(name, 0) + 1
                    total_objects += 1
            except:
                print(f"Failed to parse XML: {xml_file}")
                
    elif '.txt' in annotation_formats:
        # Assuming YOLO format
        for txt_file in annotation_files:
            if not txt_file.endswith('.txt'): continue
            try:
                with open(txt_file, 'r') as f:
                    for line in f:
                        parts = line.strip().split()
                        if parts:
                            cls_id = parts[0]
                            classes[cls_id] = classes.get(cls_id, 0) + 1
                            total_objects += 1
            except:
                pass
                
    print(f"Total labeled objects: {total_objects}")
    print("Classes found and counts:")
    for c, count in classes.items():
        print(f"  - {c}: {count}")

    # Check matching images/annotations
    img_basenames = set([os.path.splitext(os.path.basename(f))[0] for f in valid_images])
    ann_basenames = set([os.path.splitext(os.path.basename(f))[0] for f in annotation_files])
    
    images_without_annotations = img_basenames - ann_basenames
    annotations_without_images = ann_basenames - img_basenames
    
    print(f"Images without annotations: {len(images_without_annotations)}")
    print(f"Annotations without images: {len(annotations_without_images)}")

if __name__ == "__main__":
    inspect()
