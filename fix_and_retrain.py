import os
import glob
import json
import yaml
import random
import shutil
from collections import Counter
from ultralytics import YOLO

base_dir = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM"
orig_dataset = r"c:\Users\kavi priya\Downloads\Open-Pit-Mine-Object-Detection-Dataset\Open-Pit-Mine-Object-Detection-Dataset"
images_dir = os.path.join(orig_dataset, "images")
ann_dir = os.path.join(orig_dataset, "annotation")

yolo_dataset_dir = os.path.join(base_dir, "dataset", "yolo_dataset_v2")

# Create directories
for split in ['train', 'val', 'test']:
    os.makedirs(os.path.join(yolo_dataset_dir, 'images', split), exist_ok=True)
    os.makedirs(os.path.join(yolo_dataset_dir, 'labels', split), exist_ok=True)

# 1. Discover True Labels
json_files = glob.glob(os.path.join(ann_dir, "*.json"))
labels_counter = Counter()

for jf in json_files:
    try:
        with open(jf, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for shape in data.get('shapes', []):
                label = shape.get('label')
                label_str = str(label) if not isinstance(label, str) else label
                labels_counter[label_str] += 1
    except Exception as e:
        pass

unique_labels = sorted(list(labels_counter.keys()))
class_mapping = {lbl: i for i, lbl in enumerate(unique_labels)}

print("===== ORIGINAL JSON LABELS =====")
print(f"Unique labels: {unique_labels}")
print("Label counts:")
for lbl, count in labels_counter.items():
    print(f"  {repr(lbl)}: {count}")

print("\n===== CORRECTED YOLO MAPPING =====")
print(f"Class IDs: {list(class_mapping.values())}")
print(f"Class names: {list(class_mapping.keys())}")

# 2. Conversion and Validation
random.seed(42)
random.shuffle(json_files)

num_total = len(json_files)
train_split = int(0.8 * num_total)
val_split = int(0.1 * num_total)

splits = {
    'train': json_files[:train_split],
    'val': json_files[train_split:train_split + val_split],
    'test': json_files[train_split + val_split:]
}

invalid_boxes = 0

for split_name, files in splits.items():
    for jf in files:
        with open(jf, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        img_filename = os.path.basename(jf).replace('.json', '.jpg')
        img_path = os.path.join(images_dir, img_filename)
        
        if not os.path.exists(img_path):
            continue
            
        img_width = data.get('imageWidth')
        img_height = data.get('imageHeight')
        
        if not img_width or not img_height:
            continue
            
        yolo_annotations = []
        for shape in data.get('shapes', []):
            label = shape.get('label')
            label_str = str(label) if not isinstance(label, str) else label
            class_id = class_mapping[label_str]
            
            points = shape.get('points', [])
            if len(points) >= 2:
                xs = [p[0] for p in points]
                ys = [p[1] for p in points]
                xmin, xmax = min(xs), max(xs)
                ymin, ymax = min(ys), max(ys)
                
                # YOLO format: x_center, y_center, width, height (normalized)
                x_center = ((xmin + xmax) / 2) / img_width
                y_center = ((ymin + ymax) / 2) / img_height
                width = (xmax - xmin) / img_width
                height = (ymax - ymin) / img_height
                
                # Validation
                if 0 < x_center < 1 and 0 < y_center < 1 and 0 < width <= 1 and 0 < height <= 1:
                    yolo_annotations.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
                else:
                    invalid_boxes += 1
                    
        # Write files
        dest_img = os.path.join(yolo_dataset_dir, 'images', split_name, img_filename)
        dest_txt = os.path.join(yolo_dataset_dir, 'labels', split_name, img_filename.replace('.jpg', '.txt'))
        
        shutil.copy2(img_path, dest_img)
        with open(dest_txt, 'w', encoding='utf-8') as f:
            f.write('\n'.join(yolo_annotations))

if invalid_boxes > 0:
    print(f"Removed {invalid_boxes} invalid bounding boxes during conversion.")

# Generate data.yaml
data_yaml_path = os.path.join(yolo_dataset_dir, 'data.yaml')
yaml_content = {
    'train': os.path.join(yolo_dataset_dir, 'images', 'train'),
    'val': os.path.join(yolo_dataset_dir, 'images', 'val'),
    'test': os.path.join(yolo_dataset_dir, 'images', 'test'),
    'names': {i: name for name, i in class_mapping.items()}
}
with open(data_yaml_path, 'w', encoding='utf-8') as f:
    yaml.dump(yaml_content, f, allow_unicode=True)

# 3. Retrain YOLOv8n
print("\n===== TRAINING =====")
runs_dir = os.path.join(base_dir, "runs", "detect")
model = YOLO('yolov8n.pt')
results = model.train(
    data=data_yaml_path, 
    epochs=10, 
    imgsz=640, 
    batch=16, 
    project=runs_dir, 
    name="yolo_corrected",
    device='cpu',
    exist_ok=True
)

# 4. Save best model and evaluate
new_best_pt = os.path.join(runs_dir, "yolo_corrected", "weights", "best.pt")
final_model_path = os.path.join(base_dir, "models", "best.pt")

if os.path.exists(new_best_pt):
    shutil.copy2(new_best_pt, final_model_path)
    print(f"Model: YOLOv8n")
    print(f"Epochs: 10")
    print(f"Device: cpu")
    print(f"Best model: {final_model_path}")
    
    # Save metrics
    metrics = {
        "metrics/precision(B)": results.results_dict.get("metrics/precision(B)", 0),
        "metrics/recall(B)": results.results_dict.get("metrics/recall(B)", 0),
        "metrics/mAP50(B)": results.results_dict.get("metrics/mAP50(B)", 0),
        "metrics/mAP50-95(B)": results.results_dict.get("metrics/mAP50-95(B)", 0),
    }
    with open(os.path.join(base_dir, "models", "metrics.json"), "w") as f:
        json.dump(metrics, f)
        
    print("\n===== REAL METRICS =====")
    print(f"Precision: {metrics['metrics/precision(B)']:.4f}")
    print(f"Recall: {metrics['metrics/recall(B)']:.4f}")
    print(f"mAP50: {metrics['metrics/mAP50(B)']:.4f}")
    print(f"mAP50-95: {metrics['metrics/mAP50-95(B)']:.4f}")
    
    print("\n===== TEST INFERENCE =====")
    test_model = YOLO(final_model_path)
    test_images = glob.glob(os.path.join(yolo_dataset_dir, "images", "test", "*.jpg"))
    if test_images:
        test_img = test_images[0]
        print(f"Image: {test_img}")
        res = test_model(test_img)
        for r in res:
            classes = [test_model.names[int(c)] for c in r.boxes.cls]
            confs = [round(float(c), 4) for c in r.boxes.conf]
            bboxes = [[round(x, 2) for x in b] for b in r.boxes.xyxy.tolist()]
            
            print(f"Detected classes: {classes}")
            print(f"Confidence: {confs}")
            print(f"Bounding boxes: {bboxes}")

else:
    print("Training failed to produce best.pt")

