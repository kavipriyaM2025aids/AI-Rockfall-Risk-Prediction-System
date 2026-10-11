import os
import cv2
from ultralytics import YOLO

class YoloService:
    def __init__(self):
        self.model = None
        self.model_path = r"c:\Users\kavi priya\OneDrive\Documents\Desktop\AI ROCKFALL RISK PREDICTION SYSTEM\backend\runs\detect\rockguard_yolov11\weights\best.pt"
        self.is_loaded = False
        self.names = {}
        
    def load_model(self):
        if not os.path.exists(self.model_path):
            print(f"Model checkpoint not found at: {self.model_path}")
            return False
            
        try:
            self.model = YOLO(self.model_path)
            self.names = self.model.names
            self.is_loaded = True
            print("YOLOv11 model loaded successfully.")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

    def predict(self, image_path, output_annotated_path):
        if not self.is_loaded or self.model is None:
            raise ValueError("Model is not loaded.")
            
        # Run inference
        results = self.model(image_path, verbose=False)
        
        detected_classes = []
        confidences = []
        bboxes = []
        detections = []
        
        # Load image with cv2 to annotate
        img_cv2 = cv2.imread(image_path)
        
        for r in results:
            for box in r.boxes:
                class_id = int(box.cls)
                class_name = self.names[class_id]
                conf = float(box.conf)
                xyxy = box.xyxy[0].tolist()
                
                detected_classes.append(class_name)
                confidences.append(conf)
                bboxes.append(xyxy)
                
                detections.append({
                    "class_id": class_id,
                    "class_name": class_name,
                    "confidence": round(conf, 3),
                    "bbox": {
                        "x1": round(xyxy[0], 2),
                        "y1": round(xyxy[1], 2),
                        "x2": round(xyxy[2], 2),
                        "y2": round(xyxy[3], 2)
                    }
                })
                
                # Draw bounding box
                if img_cv2 is not None:
                    x1, y1, x2, y2 = map(int, xyxy)
                    label = f"Class {class_id} ({class_name}): {conf:.2f}"
                    cv2.rectangle(img_cv2, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(img_cv2, label, (x1, max(y1 - 10, 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
        # Save annotated image
        if img_cv2 is not None:
            cv2.imwrite(output_annotated_path, img_cv2)
        
        return {
            "detected_classes": detected_classes,
            "confidences": confidences,
            "bboxes": bboxes,
            "detections": detections,
            "detection_count": len(detections),
            "image_width": img_cv2.shape[1] if img_cv2 is not None else 0,
            "image_height": img_cv2.shape[0] if img_cv2 is not None else 0
        }

yolo_service = YoloService()
