import os
import json
import random
import shutil
from pathlib import Path

def convert_to_yolo():
    source_dir = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\dataset\Open-Pit-Mine-Object-Detection-Dataset\Open-Pit-Mine-Object-Detection-Dataset"
    target_dir = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\dataset\yolo_dataset"
    
    images_source = os.path.join(source_dir, "images")
    annotations_source = os.path.join(source_dir, "annotation")
    
    # Create target directories
    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(target_dir, 'images', split), exist_ok=True)
        os.makedirs(os.path.join(target_dir, 'labels', split), exist_ok=True)
        
    # Get all valid images
    all_images = [f for f in os.listdir(images_source) if f.endswith('.jpg')]
    
    # Shuffle for random split
    random.seed(42)
    random.shuffle(all_images)
    
    num_images = len(all_images)
    train_end = int(num_images * 0.8)
    val_end = int(num_images * 0.9)
    
    train_images = all_images[:train_end]
    val_images = all_images[train_end:val_end]
    test_images = all_images[val_end:]
    
    splits = {
        'train': train_images,
        'val': val_images,
        'test': test_images
    }
    
    class_mapping = {'1': 0, 'n': 1, '': 2, "'": 3}
    
    invalid_bboxes = 0
    total_processed = 0
    
    for split_name, imgs in splits.items():
        for img_name in imgs:
            base_name = os.path.splitext(img_name)[0]
            json_name = base_name + '.json'
            
            src_img = os.path.join(images_source, img_name)
            src_json = os.path.join(annotations_source, json_name)
            
            dst_img = os.path.join(target_dir, 'images', split_name, img_name)
            dst_txt = os.path.join(target_dir, 'labels', split_name, base_name + '.txt')
            
            # Copy image
            if not os.path.exists(dst_img):
                shutil.copy(src_img, dst_img)
            
            # Parse JSON and write YOLO txt
            if os.path.exists(src_json):
                with open(src_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                img_w = data.get('imageWidth', 1024)
                img_h = data.get('imageHeight', 1024)
                
                yolo_lines = []
                for shape in data.get('shapes', []):
                    label = str(shape.get('label'))
                    if label not in class_mapping:
                        continue
                        
                    class_id = class_mapping[label]
                    
                    points = shape.get('points', [])
                    if len(points) == 2:
                        p1, p2 = points
                        x_min = min(p1[0], p2[0])
                        y_min = min(p1[1], p2[1])
                        x_max = max(p1[0], p2[0])
                        y_max = max(p1[1], p2[1])
                        
                        # Validate
                        if x_min < 0 or y_min < 0 or x_max > img_w or y_max > img_h or x_min >= x_max or y_min >= y_max:
                            invalid_bboxes += 1
                            continue
                            
                        # YOLO format: class_id center_x center_y width height (normalized)
                        w = x_max - x_min
                        h = y_max - y_min
                        cx = x_min + w / 2.0
                        cy = y_min + h / 2.0
                        
                        nx = cx / img_w
                        ny = cy / img_h
                        nw = w / img_w
                        nh = h / img_h
                        
                        yolo_lines.append(f"{class_id} {nx:.6f} {ny:.6f} {nw:.6f} {nh:.6f}")
                
                with open(dst_txt, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(yolo_lines))
                total_processed += 1
                
    # Write data.yaml
    yaml_content = f"""path: {target_dir}
train: images/train
val: images/val
test: images/test

names:
  0: '1'
  1: 'n'
  2: ''
  3: "'"
"""
    with open(os.path.join(target_dir, 'data.yaml'), 'w', encoding='utf-8') as f:
        f.write(yaml_content)
        
    print(f"YOLO dataset preparation complete.")
    print(f"Total processed: {total_processed}")
    print(f"Train: {len(train_images)}, Val: {len(val_images)}, Test: {len(test_images)}")

if __name__ == "__main__":
    convert_to_yolo()
