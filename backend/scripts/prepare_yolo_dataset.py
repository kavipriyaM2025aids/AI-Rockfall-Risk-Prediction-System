import os
import glob
import json
import random
import shutil
import datetime

def prepare_yolo():
    original_dataset_path = r"C:\Users\kavi priya\Downloads\Open-Pit-Mine-Object-Detection-Dataset\Open-Pit-Mine-Object-Detection-Dataset"
    original_images_dir = os.path.join(original_dataset_path, "images")
    original_annotations_dir = os.path.join(original_dataset_path, "annotation")
    
    yolo_dir = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\backend\dataset\yolo"
    
    # Clean previous yolo dir if exists to avoid overlap
    if os.path.exists(yolo_dir):
        shutil.rmtree(yolo_dir)
        
    # Create directories
    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(yolo_dir, 'images', split), exist_ok=True)
        os.makedirs(os.path.join(yolo_dir, 'labels', split), exist_ok=True)
        
    json_files = glob.glob(os.path.join(original_annotations_dir, "**", "*.json"), recursive=True)
    json_files.sort()  # ensure determinism
    
    class_mapping = {
        '1': 0,
        'n': 1
    }
    
    excluded_empty = []
    excluded_apostrophe = []
    corrected_bboxes = []
    removed_invalid_bboxes = []
    
    valid_data = [] # list of dicts: {'json_path', 'img_path', 'img_w', 'img_h', 'yolo_labels'}
    
    class_counts = {0: 0, 1: 0}
    
    for jf in json_files:
        with open(jf, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        img_basename = os.path.basename(jf).replace('.json', '')
        img_path = os.path.join(original_images_dir, img_basename + ".jpg")
        
        if not os.path.exists(img_path):
            continue
            
        img_width = data.get('imageWidth', 1024)
        img_height = data.get('imageHeight', 1024)
        
        yolo_labels = []
        
        for shape in data.get('shapes', []):
            label = str(shape.get('label', '')).strip()
            
            # Map weird unicode empty label to standard empty
            if label not in ['1', 'n', "'"]:
                label = ''
                
            if label == '':
                excluded_empty.append({'image': img_basename, 'points': shape.get('points')})
                continue
            elif label == "'":
                excluded_apostrophe.append({'image': img_basename, 'points': shape.get('points')})
                continue
                
            class_id = class_mapping[label]
            
            points = shape.get('points', [])
            if len(points) == 2:
                p1, p2 = points
                x_min = min(p1[0], p2[0])
                y_min = min(p1[1], p2[1])
                x_max = max(p1[0], p2[0])
                y_max = max(p1[1], p2[1])
                
                # Check for OOB and correct
                orig_bbox = [x_min, y_min, x_max, y_max]
                is_oob = False
                
                if x_min < 0: x_min = 0; is_oob = True
                if y_min < 0: y_min = 0; is_oob = True
                if x_max > img_width: x_max = img_width; is_oob = True
                if y_max > img_height: y_max = img_height; is_oob = True
                
                if is_oob:
                    if x_max > x_min and y_max > y_min:
                        corrected_bboxes.append({
                            'image': img_basename,
                            'original': orig_bbox,
                            'corrected': [x_min, y_min, x_max, y_max]
                        })
                    else:
                        removed_invalid_bboxes.append({
                            'image': img_basename,
                            'original': orig_bbox,
                            'reason': 'Zero or negative dimensions after clipping'
                        })
                        continue
                        
                # Validate dimensions
                if x_max <= x_min or y_max <= y_min:
                    removed_invalid_bboxes.append({
                        'image': img_basename,
                        'original': orig_bbox,
                        'reason': 'Zero or negative dimensions'
                    })
                    continue
                    
                # Calculate YOLO format
                x_center = (x_min + x_max) / 2.0 / img_width
                y_center = (y_min + y_max) / 2.0 / img_height
                width = (x_max - x_min) / img_width
                height = (y_max - y_min) / img_height
                
                # strict normalization bounds check
                x_center = max(0.0, min(1.0, x_center))
                y_center = max(0.0, min(1.0, y_center))
                width = max(0.0, min(1.0, width))
                height = max(0.0, min(1.0, height))
                
                yolo_labels.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
                class_counts[class_id] += 1
                
        if yolo_labels:
            valid_data.append({
                'json_path': jf,
                'img_path': img_path,
                'img_basename': img_basename,
                'yolo_labels': yolo_labels
            })
            
    # Split Dataset
    random.seed(42)
    random.shuffle(valid_data)
    
    n_total = len(valid_data)
    n_train = int(0.7 * n_total)
    n_val = int(0.2 * n_total)
    
    splits = {
        'train': valid_data[:n_train],
        'val': valid_data[n_train:n_train + n_val],
        'test': valid_data[n_train + n_val:]
    }
    
    split_counts = {'train': len(splits['train']), 'val': len(splits['val']), 'test': len(splits['test'])}
    label_counts_split = {'train': 0, 'val': 0, 'test': 0}
    
    # Process files
    for split_name, items in splits.items():
        for item in items:
            dest_img = os.path.join(yolo_dir, 'images', split_name, item['img_basename'] + '.jpg')
            dest_txt = os.path.join(yolo_dir, 'labels', split_name, item['img_basename'] + '.txt')
            
            shutil.copy2(item['img_path'], dest_img)
            with open(dest_txt, 'w', encoding='utf-8') as f:
                f.write("\n".join(item['yolo_labels']) + "\n")
                
            label_counts_split[split_name] += len(item['yolo_labels'])
            
    # Generate data.yaml
    data_yaml_content = f"""path: {yolo_dir}
train: images/train
val: images/val
test: images/test

nc: 2
names:
  0: class_1
  1: class_n
"""
    with open(os.path.join(yolo_dir, 'data.yaml'), 'w') as f:
        f.write(data_yaml_content)
        
    # Validation step
    print("Validating dataset...")
    for split_name in ['train', 'val', 'test']:
        txt_files = glob.glob(os.path.join(yolo_dir, 'labels', split_name, '*.txt'))
        for tf in txt_files:
            with open(tf, 'r') as f:
                lines = f.readlines()
            for line in lines:
                parts = line.strip().split()
                if len(parts) != 5:
                    print(f"Validation Error: Invalid label format in {tf}")
                cid = int(parts[0])
                if cid not in [0, 1]:
                    print(f"Validation Error: Invalid class ID {cid} in {tf}")
                coords = [float(p) for p in parts[1:]]
                for c in coords:
                    if c < 0.0 or c > 1.0:
                        print(f"Validation Error: Coordinate out of bounds in {tf}")
                if coords[2] <= 0 or coords[3] <= 0:
                    print(f"Validation Error: Zero/negative width or height in {tf}")
                    
    # Generate reports
    report_dict = {
        'preprocessing_timestamp': datetime.datetime.now().isoformat(),
        'random_seed': 42,
        'original_image_count': len(glob.glob(os.path.join(original_images_dir, "**", "*.jpg"), recursive=True)),
        'original_annotation_count': len(json_files),
        'class_mapping': class_mapping,
        'valid_class_counts': {
            'class_1_id_0': class_counts[0],
            'class_n_id_1': class_counts[1]
        },
        'excluded_label_counts': {
            'empty': len(excluded_empty),
            'apostrophe': len(excluded_apostrophe)
        },
        'corrected_oob_boxes': len(corrected_bboxes),
        'removed_invalid_boxes': len(removed_invalid_bboxes),
        'split_image_counts': split_counts,
        'split_label_counts': label_counts_split,
        'class_distribution': {
            'class_1_id_0': f"{(class_counts[0]/max(1, sum(class_counts.values())))*100:.2f}%",
            'class_n_id_1': f"{(class_counts[1]/max(1, sum(class_counts.values())))*100:.2f}%"
        },
        'excluded_empty': excluded_empty,
        'excluded_apostrophe': excluded_apostrophe,
        'corrected_bboxes': corrected_bboxes,
        'removed_invalid_bboxes': removed_invalid_bboxes
    }
    
    with open(os.path.join(yolo_dir, 'preprocessing_report.json'), 'w') as f:
        json.dump(report_dict, f, indent=4)
        
    report_txt = f"""DATASET PREPARATION COMPLETE
============================
Original images: {report_dict['original_image_count']}
Original JSON files: {report_dict['original_annotation_count']}

Valid class 1 objects: {class_counts[0]}
Valid class n objects: {class_counts[1]}

Empty labels excluded: {len(excluded_empty)}
Apostrophe labels excluded: {len(excluded_apostrophe)}

OOB boxes corrected: {len(corrected_bboxes)}
Invalid boxes removed: {len(removed_invalid_bboxes)}

Train images: {split_counts['train']}
Validation images: {split_counts['val']}
Test images: {split_counts['test']}

Train labels: {label_counts_split['train']}
Validation labels: {label_counts_split['val']}
Test labels: {label_counts_split['test']}

Output:
{yolo_dir}
"""
    with open(os.path.join(yolo_dir, 'preprocessing_report.txt'), 'w') as f:
        f.write(report_txt)
        
    print(report_txt)

if __name__ == '__main__':
    prepare_yolo()
