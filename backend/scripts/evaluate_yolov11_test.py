import os
import sys
import json
import torch
from ultralytics import YOLO

def main():
    base_dir = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\backend"
    runs_dir = os.path.join(base_dir, "runs", "detect", "rockguard_yolov11")
    weights_dir = os.path.join(runs_dir, "weights")
    
    best_pt = os.path.join(weights_dir, "best.pt")
    last_pt = os.path.join(weights_dir, "last.pt")
    
    print("Inspecting checkpoints...")
    best_fitness = -1.0
    last_fitness = -1.0
    best_epoch = -1
    last_epoch = -1
    
    if os.path.exists(best_pt):
        ckpt = torch.load(best_pt, map_location='cpu', weights_only=False)
        best_fitness = ckpt.get('best_fitness', -1.0)
        best_epoch = ckpt.get('epoch', -1)
        print(f"best.pt exists | Epoch: {best_epoch} | Fitness: {best_fitness:.5f} | Size: {os.path.getsize(best_pt)} bytes")
    
    if os.path.exists(last_pt):
        ckpt = torch.load(last_pt, map_location='cpu', weights_only=False)
        last_fitness = ckpt.get('best_fitness', -1.0) 
        last_epoch = ckpt.get('epoch', -1)
        print(f"last.pt exists | Epoch: {last_epoch} | Fitness: {last_fitness:.5f} | Size: {os.path.getsize(last_pt)} bytes")
        
    selected_ckpt = best_pt
    selected_epoch = best_epoch
    if last_fitness > best_fitness and os.path.exists(last_pt):
        selected_ckpt = last_pt
        selected_epoch = last_epoch
    elif not os.path.exists(best_pt) and os.path.exists(last_pt):
        selected_ckpt = last_pt
        selected_epoch = last_epoch
        
    print(f"Selected checkpoint for evaluation: {selected_ckpt}")
    
    # Verify dataset
    data_yaml = os.path.join(base_dir, "dataset", "yolo", "data.yaml")
    test_images_dir = os.path.join(base_dir, "dataset", "yolo", "images", "test")
    test_labels_dir = os.path.join(base_dir, "dataset", "yolo", "labels", "test")
    
    if not os.path.exists(data_yaml):
        print(f"ERROR: data.yaml not found at {data_yaml}")
        sys.exit(1)
    if not os.path.exists(test_images_dir):
        print(f"ERROR: Test images directory not found at {test_images_dir}")
        sys.exit(1)
    if not os.path.exists(test_labels_dir):
        print(f"ERROR: Test labels directory not found at {test_labels_dir}")
        sys.exit(1)
        
    test_images_count = len([f for f in os.listdir(test_images_dir) if f.endswith('.jpg') or f.endswith('.png')])
    test_labels_count = len([f for f in os.listdir(test_labels_dir) if f.endswith('.txt')])
    print(f"Verified: {test_images_count} test images, {test_labels_count} test labels.")
    
    if test_images_count == 0:
        print("ERROR: No test images found!")
        sys.exit(1)
        
    # Load model
    print("Loading model...")
    model = YOLO(selected_ckpt)
    
    print("Running evaluation on test split...")
    metrics = model.val(
        data=data_yaml,
        split='test',
        project=os.path.join(base_dir, "runs", "detect"),
        name="rockguard_yolov11_test",
        exist_ok=True,
        device="cpu",
        plots=True,
        workers=0
    )
    
    results_dict = metrics.results_dict
    overall_p = results_dict.get('metrics/precision(B)', 0.0)
    overall_r = results_dict.get('metrics/recall(B)', 0.0)
    overall_map50 = results_dict.get('metrics/mAP50(B)', 0.0)
    overall_map = results_dict.get('metrics/mAP50-95(B)', 0.0)
    
    box = metrics.box
    ap_classes = box.ap_class_index.tolist()
    
    class_metrics = {}
    for i, cls_idx in enumerate(ap_classes):
        class_metrics[cls_idx] = {
            'precision': float(box.p[i]),
            'recall': float(box.r[i]),
            'mAP50': float(box.map50[i]),
            'mAP50-95': float(box.map[i])
        }
        
    c0 = class_metrics.get(0, {'precision': 0.0, 'recall': 0.0, 'mAP50': 0.0, 'mAP50-95': 0.0})
    c1 = class_metrics.get(1, {'precision': 0.0, 'recall': 0.0, 'mAP50': 0.0, 'mAP50-95': 0.0})
    
    output_dir = os.path.join(base_dir, "runs", "detect", "rockguard_yolov11_test")
    os.makedirs(output_dir, exist_ok=True)
    
    json_path = os.path.join(output_dir, "test_metrics.json")
    txt_path = os.path.join(output_dir, "test_metrics.txt")
    
    report_data = {
        "model_checkpoint": selected_ckpt,
        "model_name": "YOLOv11 Nano",
        "training_epoch": selected_epoch,
        "test_image_count": test_images_count,
        "test_label_count": test_labels_count,
        "class_names": model.names,
        "test_dataset_path": test_images_dir,
        "overall": {
            "precision": overall_p,
            "recall": overall_r,
            "mAP50": overall_map50,
            "mAP50_95": overall_map
        },
        "per_class": {
            "0": c0,
            "1": c1
        }
    }
    
    with open(json_path, 'w') as f:
        json.dump(report_data, f, indent=4)
        
    txt_content = f"""MODEL CHECKPOINT
- checkpoint path: {selected_ckpt}
- model name: YOLOv11 Nano
- training epoch: {selected_epoch}

DATASET
- test image count: {test_images_count}
- test label count: {test_labels_count}
- class names: {model.names}
- test dataset path: {test_images_dir}

RESULTS
- Precision: {overall_p:.5f}
- Recall: {overall_r:.5f}
- mAP@50: {overall_map50:.5f}
- mAP@50–95: {overall_map:.5f}

PER-CLASS RESULTS
- Class 0 / original label "1": Precision={c0['precision']:.5f}, Recall={c0['recall']:.5f}, mAP50={c0['mAP50']:.5f}, mAP50-95={c0['mAP50-95']:.5f}
- Class 1 / original label "n": Precision={c1['precision']:.5f}, Recall={c1['recall']:.5f}, mAP50={c1['mAP50']:.5f}, mAP50-95={c1['mAP50-95']:.5f}
"""

    with open(txt_path, 'w') as f:
        f.write(txt_content)
        
    print("\n========================================")
    print("YOLOv11 TEST EVALUATION COMPLETE")
    print(f"Checkpoint: {selected_ckpt}")
    print(f"Epoch: {selected_epoch}")
    print(f"\nTest Images: {test_images_count}")
    print(f"\nPrecision: {overall_p:.5f}")
    print(f"Recall: {overall_r:.5f}")
    print(f"mAP@50: {overall_map50:.5f}")
    print(f"mAP@50-95: {overall_map:.5f}")
    print("\nClass 0 (\"1\"):")
    print(f"Precision: {c0['precision']:.5f}")
    print(f"Recall: {c0['recall']:.5f}")
    print(f"mAP50: {c0['mAP50']:.5f}")
    print(f"mAP50-95: {c0['mAP50-95']:.5f}")
    print("\nClass 1 (\"n\"):")
    print(f"Precision: {c1['precision']:.5f}")
    print(f"Recall: {c1['recall']:.5f}")
    print(f"mAP50: {c1['mAP50']:.5f}")
    print(f"mAP50-95: {c1['mAP50-95']:.5f}")
    
    cm_path = os.path.join(output_dir, "confusion_matrix.png")
    print(f"\nConfusion Matrix: {'Generated at ' + cm_path if os.path.exists(cm_path) else 'Not generated'}")
    print(f"Results Directory: {output_dir}")
    print("========================================")

if __name__ == "__main__":
    main()
