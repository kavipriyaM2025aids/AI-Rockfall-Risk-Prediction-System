from ultralytics import YOLO
import os
import glob
import json

base_dir = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM"
model_path = os.path.join(base_dir, "models", "best.pt")
test_images_dir = os.path.join(base_dir, "dataset", "yolo_dataset", "images", "test")

# Load model
model = YOLO(model_path)

# Pick a test image
test_images = glob.glob(os.path.join(test_images_dir, "*.jpg"))
if not test_images:
    print("No test images found.")
    exit()

image_path = test_images[0]
print(f"Running prediction on: {os.path.basename(image_path)}")

# Predict
results = model(image_path)

print("\n--- REAL TEST PREDICTION ---")
for r in results:
    if len(r.boxes) == 0:
        print("No objects detected in this image.")
    for box in r.boxes:
        cls_id = int(box.cls)
        cls_name = model.names[cls_id]
        conf = float(box.conf)
        bbox = box.xyxy[0].tolist()
        print(f"Detected Class: '{cls_name}'")
        print(f"Confidence: {conf*100:.2f}%")
        print(f"Bounding Box: [xmin: {bbox[0]:.1f}, ymin: {bbox[1]:.1f}, xmax: {bbox[2]:.1f}, ymax: {bbox[3]:.1f}]")
        print("-" * 30)
