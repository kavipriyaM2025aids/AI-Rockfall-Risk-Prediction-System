import os
import glob
import json
from collections import Counter
from PIL import Image

def inspect():
    dataset_path = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\dataset\Open-Pit-Mine-Object-Detection-Dataset\Open-Pit-Mine-Object-Detection-Dataset"
    
    images_dir = os.path.join(dataset_path, "images")
    annotations_dir = os.path.join(dataset_path, "annotation")
    
    image_files = glob.glob(os.path.join(images_dir, "**", "*.*"), recursive=True)
    json_files = glob.glob(os.path.join(annotations_dir, "**", "*.json"), recursive=True)
    
    print(f"1. Total images found: {len(image_files)}")
    print(f"2. Total JSON annotations found: {len(json_files)}")
    
    # Check for train/val/test splits
    subdirs = set()
    for root, dirs, files in os.walk(images_dir):
        for d in dirs:
            subdirs.add(d.lower())
    
    print(f"11. Train/val/test splits existing in images dir: {subdirs if subdirs else 'No subdirectories found, likely all in one folder.'}")
    
    classes = Counter()
    corrupted_jsons = []
    invalid_bboxes = 0
    total_bboxes = 0
    
    image_formats = set()
    image_dimensions = set()
    valid_images = []
    
    for img_path in image_files:
        ext = os.path.splitext(img_path)[1].lower()
        image_formats.add(ext)
        if ext in ['.jpg', '.jpeg', '.png']:
            try:
                with Image.open(img_path) as img:
                    image_dimensions.add(img.size)
                    valid_images.append(img_path)
            except Exception as e:
                pass
                
    print(f"5. Image formats: {list(image_formats)}")
    print(f"6. Unique image dimensions (first 5): {list(image_dimensions)[:5]}")

    for jf in json_files:
        try:
            with open(jf, 'r', encoding='utf-8') as f:
                data = json.load(f)
                img_width = data.get('imageWidth', 1024)
                img_height = data.get('imageHeight', 1024)
                
                for shape in data.get('shapes', []):
                    label = str(shape.get('label'))
                    classes[label] += 1
                    total_bboxes += 1
                    
                    points = shape.get('points', [])
                    if len(points) == 2:
                        p1, p2 = points
                        x_min = min(p1[0], p2[0])
                        y_min = min(p1[1], p2[1])
                        x_max = max(p1[0], p2[0])
                        y_max = max(p1[1], p2[1])
                        
                        # Check validity
                        if x_min < 0 or y_min < 0 or x_max > img_width or y_max > img_height or x_min >= x_max or y_min >= y_max:
                            invalid_bboxes += 1
                    else:
                        invalid_bboxes += 1 # Not a rectangle with 2 points
                        
        except Exception as e:
            corrupted_jsons.append(jf)
            
    print(f"3. All unique class labels: {list(classes.keys())}")
    print(f"4. Number of annotations per class: {dict(classes)}")
    
    print(f"8. Corrupted annotations: {len(corrupted_jsons)}")
    print(f"9. Invalid bounding boxes: {invalid_bboxes} out of {total_bboxes}")
    
    # 10. Class imbalance
    print("10. Dataset class imbalance:")
    for cls, count in classes.items():
        percentage = (count / total_bboxes) * 100 if total_bboxes > 0 else 0
        print(f"   - {cls}: {percentage:.2f}%")
        
    img_basenames = set([os.path.splitext(os.path.basename(f))[0] for f in image_files])
    ann_basenames = set([os.path.splitext(os.path.basename(f))[0] for f in json_files])
    
    images_without_annotations = img_basenames - ann_basenames
    annotations_without_images = ann_basenames - img_basenames
    
    print(f"7. Images without annotations: {len(images_without_annotations)}")
    print(f"7. Annotations without images: {len(annotations_without_images)}")

if __name__ == "__main__":
    inspect()
