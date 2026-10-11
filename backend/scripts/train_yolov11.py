import os
import sys
import json
import time
import datetime
from pathlib import Path
try:
    from ultralytics import YOLO
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "ultralytics"])
    from ultralytics import YOLO

import torch
import ultralytics

def run_training():
    start_time = time.time()
    
    yolo_dir = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\backend\dataset\yolo"
    data_yaml = os.path.join(yolo_dir, "data.yaml")
    
    print("Python version:", sys.version)
    print("Ultralytics version:", ultralytics.__version__)
    print("PyTorch version:", torch.__version__)
    print("CUDA availability:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("GPU name:", torch.cuda.get_device_name(0))
        device = 0
        batch_size = -1  # auto batch
    else:
        print("GPU name: N/A")
        device = 'cpu'
        batch_size = 16  # fixed batch size for cpu to avoid auto batching hangs
        
    print("Dataset path:", yolo_dir)
    print("Number of classes: 2")
    print("Class names: ['class_1', 'class_n']")
    
    # Start with standard YOLOv11n weights
    model = YOLO("yolo11n.pt")
    
    project_dir = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\backend\runs\detect"
    
    print("Starting training...")
    results = model.train(
        data=data_yaml,
        epochs=50,
        imgsz=640,
        batch=batch_size,
        seed=42,
        patience=15,
        project=project_dir,
        name="rockguard_yolov11",
        device=device,
        exist_ok=True,
        workers=0 if sys.platform == 'win32' else 4 # safe for windows
    )
    
    best_model_path = os.path.join(project_dir, "rockguard_yolov11", "weights", "best.pt")
    
    print("Running evaluation on TEST set...")
    test_results = model.val(
        data=data_yaml, 
        split='test', 
        project=project_dir, 
        name="rockguard_yolov11_test", 
        device=device, 
        exist_ok=True,
        workers=0 if sys.platform == 'win32' else 4
    )
    
    # Ultralytics val() returns a metrics object
    metrics = test_results.results_dict
    
    precision = metrics.get('metrics/precision(B)', 0.0)
    recall = metrics.get('metrics/recall(B)', 0.0)
    map50 = metrics.get('metrics/mAP50(B)', 0.0)
    map50_95 = metrics.get('metrics/mAP50-95(B)', 0.0)
    
    training_duration = time.time() - start_time
    
    report_dict = {
        'model': 'YOLOv11n',
        'dataset_path': yolo_dir,
        'class_count': 2,
        'class_names': ['class_1', 'class_n'],
        'train_image_count': 3231,
        'validation_image_count': 923,
        'test_image_count': 462,
        'epochs': 50,
        'image_size': 640,
        'batch_size': batch_size if batch_size != -1 else 'auto',
        'seed': 42,
        'device': 'gpu' if torch.cuda.is_available() else 'cpu',
        'best_model_path': best_model_path,
        'precision': float(precision),
        'recall': float(recall),
        'mAP50': float(map50),
        'mAP50_95': float(map50_95),
        'training_duration_seconds': float(training_duration),
        'training_status': 'SUCCESS' if os.path.exists(best_model_path) else 'FAIL'
    }
    
    base_dir = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\backend"
    
    with open(os.path.join(base_dir, "yolo_training_report.json"), "w", encoding='utf-8') as f:
        json.dump(report_dict, f, indent=4)
        
    report_txt = f"""========================================
ROCKGUARD AI — YOLOv11 TRAINING COMPLETE
========================================

Model:
YOLOv11n

Dataset:
backend/dataset/yolo

Train images:
3231

Validation images:
923

Test images:
462

Classes:
2

Class 0:
class_1

Class 1:
class_n

Best model:
{best_model_path}

Device:
{'GPU' if torch.cuda.is_available() else 'CPU'}

Precision:
{precision:.4f}

Recall:
{recall:.4f}

mAP@0.50:
{map50:.4f}

mAP@0.50:0.95:
{map50_95:.4f}

Training status:
{report_dict['training_status']}
========================================
"""
    
    with open(os.path.join(base_dir, "yolo_training_report.txt"), "w", encoding='utf-8') as f:
        f.write(report_txt)
        
    print(report_txt)

if __name__ == "__main__":
    run_training()
