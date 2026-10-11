import os
from ultralytics import YOLO
import glob

base_dir = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM"
model_path = os.path.join(base_dir, "models", "best.pt")

print(f"MODEL PATH: {model_path}")
print(f"MODEL EXISTS: {os.path.exists(model_path)}")

if not os.path.exists(model_path):
    print("REAL MODEL NOT TRAINED")
    exit(1)

model_size = os.path.getsize(model_path)
print(f"MODEL SIZE: {model_size / (1024*1024):.2f} MB")

try:
    model = YOLO(model_path)
    print(f"CLASS NAMES: {model.names}")
except Exception as e:
    print(f"Failed to load YOLO model: {e}")
    exit(1)

test_images_dir = os.path.join(base_dir, "dataset", "yolo_dataset", "images", "test")
test_images = glob.glob(os.path.join(test_images_dir, "*.jpg"))
if not test_images:
    print("No test images found.")
    exit(1)

image_path = test_images[0]
print(f"SOURCE IMAGE: {image_path}")

results = model(image_path)

detected_classes = []
confidences = []
bboxes = []

for r in results:
    for box in r.boxes:
        detected_classes.append(model.names[int(box.cls)])
        confidences.append(float(box.conf))
        bboxes.append(box.xyxy[0].tolist())

print(f"DETECTED CLASSES: {detected_classes}")
print(f"CONFIDENCES: {confidences}")
print(f"BOUNDING BOXES: {bboxes}")
