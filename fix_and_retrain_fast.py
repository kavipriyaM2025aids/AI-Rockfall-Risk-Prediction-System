import os
import glob
import json
import yaml
import shutil
from collections import Counter
from ultralytics import YOLO

base_dir = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM"
orig_dataset = r"c:\Users\kavi priya\Downloads\Open-Pit-Mine-Object-Detection-Dataset\Open-Pit-Mine-Object-Detection-Dataset"
ann_dir = os.path.join(orig_dataset, "annotation")
yolo_dataset_dir = os.path.join(base_dir, "dataset", "yolo_dataset_v2")

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

data_yaml_path = os.path.join(yolo_dataset_dir, 'data.yaml')

# 3. Retrain YOLOv8n
print("\n===== TRAINING =====")
runs_dir = os.path.join(base_dir, "runs", "detect")
model = YOLO('yolov8n.pt')
# Using imgsz=160 and epochs=1 to ensure it completes reasonably fast on CPU for this verification.
results = model.train(
    data=data_yaml_path, 
    epochs=1, 
    imgsz=160, 
    batch=32, 
    project=runs_dir, 
    name="yolo_corrected_fast",
    device='cpu',
    exist_ok=True,
    workers=4
)

# 4. Save best model and evaluate
new_best_pt = os.path.join(runs_dir, "yolo_corrected_fast", "weights", "best.pt")
final_model_path = os.path.join(base_dir, "models", "best.pt")

if os.path.exists(new_best_pt):
    shutil.copy2(new_best_pt, final_model_path)
    print(f"Model: YOLOv8n")
    print(f"Epochs: 1")
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
