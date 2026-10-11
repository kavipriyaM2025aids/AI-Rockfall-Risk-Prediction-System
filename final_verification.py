import os
import time
import glob
import json
import yaml
from ultralytics import YOLO
import sys

base_dir = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM"
model_path = os.path.join(base_dir, "models", "best.pt")

print("===== MODEL VERIFICATION =====")
print(f"Model: YOLOv8")
print(f"Model path: {model_path}")

if os.path.exists(model_path):
    print("Model exists: YES")
    size_mb = os.path.getsize(model_path) / (1024*1024)
    print(f"Model size: {size_mb:.2f} MB")
    try:
        model = YOLO(model_path)
        print("YOLO load successful: YES")
        print(f"Model classes: {model.names}")
    except Exception as e:
        print("YOLO load successful: NO")
        print(f"Error: {e}")
else:
    print("Model exists: NO")
    sys.exit(1)

print("\n===== DATASET =====")
orig_dataset = r"c:\Users\kavi priya\Downloads\Open-Pit-Mine-Object-Detection-Dataset\Open-Pit-Mine-Object-Detection-Dataset"
print(f"Original dataset: {orig_dataset}")

images = glob.glob(os.path.join(orig_dataset, "images", "*.jpg"))
annotations = glob.glob(os.path.join(orig_dataset, "annotation", "*.json"))
print(f"Images: {len(images)}")
print(f"Annotations: {len(annotations)}")

data_yaml = os.path.join(base_dir, "dataset", "yolo_dataset", "data.yaml")
if os.path.exists(data_yaml):
    with open(data_yaml, 'r') as f:
        dy = yaml.safe_load(f)
    print(f"Actual classes: {dy.get('names')}")
else:
    print("Actual classes: data.yaml NOT FOUND")

print("\n===== TRAINING =====")
runs_dir = os.path.join(base_dir, "runs", "detect")
train_runs = sorted(glob.glob(os.path.join(runs_dir, "train*")), key=os.path.getmtime, reverse=True)

if train_runs:
    print("Training run exists: YES")
    latest_run = train_runs[0]
    args_path = os.path.join(latest_run, "args.yaml")
    if os.path.exists(args_path):
        with open(args_path, 'r') as f:
            args = yaml.safe_load(f)
        print(f"Architecture: {args.get('model')}")
        print(f"Epochs: {args.get('epochs')}")
        print(f"Image size: {args.get('imgsz')}")
        print(f"Batch size: {args.get('batch')}")
        print(f"Device: {args.get('device')}")
    else:
        print("Architecture: Unknown")
        print("Epochs: Unknown")
        print("Image size: Unknown")
        print("Batch size: Unknown")
        print("Device: Unknown")
else:
    print("Training run exists: NO")
    print("Architecture: N/A")
    print("Epochs: N/A")
    print("Image size: N/A")
    print("Batch size: N/A")
    print("Device: N/A")

print("\n===== REAL METRICS =====")
metrics_json = os.path.join(base_dir, "models", "metrics.json")
if os.path.exists(metrics_json):
    with open(metrics_json, 'r') as f:
        metrics = json.load(f)
    # Ultralytics metrics keys can vary slightly depending on version, parsing defensively:
    p = metrics.get('metrics/precision(B)', 0)
    r = metrics.get('metrics/recall(B)', 0)
    m50 = metrics.get('metrics/mAP50(B)', 0)
    m95 = metrics.get('metrics/mAP50-95(B)', 0)
    print(f"Precision: {p:.4f}")
    print(f"Recall: {r:.4f}")
    print(f"mAP50: {m50:.4f}")
    print(f"mAP50-95: {m95:.4f}")
else:
    print("Precision: N/A")
    print("Recall: N/A")
    print("mAP50: N/A")
    print("mAP50-95: N/A")

print("\n===== REAL TEST INFERENCE =====")
test_images_dir = os.path.join(base_dir, "dataset", "yolo_dataset", "images", "test")
test_images = glob.glob(os.path.join(test_images_dir, "*.jpg"))
if test_images:
    test_image = test_images[0]
    print(f"Test image: {test_image}")
    results = model(test_image)
    for r in results:
        # Save real prediction visualization
        r.save(filename=os.path.join(base_dir, "simulation_test_output.jpg"))
        
        classes = []
        confs = []
        bboxes = []
        for box in r.boxes:
            classes.append(model.names[int(box.cls)])
            confs.append(round(float(box.conf), 4))
            bboxes.append([round(x, 2) for x in box.xyxy[0].tolist()])
        
        print(f"Detected classes: {classes}")
        print(f"Confidence: {confs}")
        print(f"Bounding boxes: {bboxes}")
else:
    print("Test image: NOT FOUND")

print("\n===== APPLICATION CONNECTION =====")
main_py = os.path.join(base_dir, "backend", "main.py")
if os.path.exists(main_py):
    with open(main_py, 'r') as f:
        content = f.read()
    
    predict_has_model = "model = YOLO(MODEL_PATH)" in content and "results = model(file_path)" in content
    sim_has_model = "model = YOLO(MODEL_PATH)" in content and "results = model(selected_image)" in content
    sqlite_real = "db_record = PredictionHistory(" in content and "detected_classes=json.dumps(detected_classes)" in content

    print(f"Image Prediction -> best.pt: {'YES' if predict_has_model else 'NO'}")
    print(f"Dataset Simulation -> best.pt: {'YES' if sim_has_model else 'NO'}")
    print(f"SQLite predictions -> real inference: {'YES' if sqlite_real else 'NO'}")

    print("\n===== HARDCODED/MOCK CHECK =====")
    has_mock_preds = "[['1', 0.85" in content or "mock" in content.lower() or "hardcoded" in content.lower()
    has_fake_metrics = "0.95" in content and "precision" in content.lower()
    has_hardcoded_conf = "confidence: 0.99" in content

    print(f"Mock predictions found: {'YES' if has_mock_preds else 'NO'}")
    print(f"Fake metrics found: {'YES' if has_fake_metrics else 'NO'}")
    print(f"Hardcoded confidence found: {'YES' if has_hardcoded_conf else 'NO'}")
else:
    print("BACKEND NOT FOUND")
