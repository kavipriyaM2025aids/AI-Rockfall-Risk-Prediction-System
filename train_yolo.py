from ultralytics import YOLO
import torch
import os
import shutil
import json

def train_model():
    base_dir = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM"
    dataset_yaml = os.path.join(base_dir, "dataset", "yolo_dataset", "data.yaml")
    models_dir = os.path.join(base_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    
    device = '0' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    # Initialize YOLOv8 nano model for speed
    model = YOLO("yolov8n.pt")
    
    # We will train for 20 epochs if GPU and 3 epochs if CPU (since 4.6k images on CPU takes very long)
    epochs = 20 if device == '0' else 2
    
    print(f"Starting training for {epochs} epochs...")
    results = model.train(
        data=dataset_yaml,
        epochs=epochs,
        imgsz=640,
        device=device,
        project=models_dir,
        name='yolo_rockfall',
        exist_ok=True,
        batch=16
    )
    
    print("Training finished.")
    
    # Copy best model to models/best.pt
    best_model_path = os.path.join(models_dir, 'yolo_rockfall', 'weights', 'best.pt')
    if os.path.exists(best_model_path):
        shutil.copy(best_model_path, os.path.join(models_dir, 'best.pt'))
        print(f"Saved best model to {os.path.join(models_dir, 'best.pt')}")
        
    print("Evaluating on test set...")
    # Load the best model for validation
    best_model = YOLO(os.path.join(models_dir, 'best.pt'))
    metrics = best_model.val(data=dataset_yaml, split='test')
    
    print("Real test metrics:")
    metrics_dict = metrics.results_dict
    print(json.dumps(metrics_dict, indent=4))
    
    # Save metrics to a file so we can display them later
    with open(os.path.join(models_dir, 'metrics.json'), 'w') as f:
        json.dump(metrics_dict, f)

if __name__ == '__main__':
    train_model()
