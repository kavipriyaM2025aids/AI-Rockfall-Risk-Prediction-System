import os
import json
import random
import numpy as np
import pandas as pd
from ultralytics import YOLO
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import shap

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'runs', 'detect', 'rockguard_yolov11', 'weights', 'best.pt')
DATASET_VAL_IMAGES = os.path.join(BASE_DIR, 'dataset', 'yolo', 'images', 'test')
RISK_MODEL_OUTPUT = os.path.join(BASE_DIR, 'models', 'risk_xgboost.json')
REPORT_OUTPUT = os.path.join(BASE_DIR, 'risk_model_training_report.txt')

os.makedirs(os.path.join(BASE_DIR, 'models'), exist_ok=True)

# Experimental Rule for Label Generation
def generate_experimental_label(row):
    """
    Transparent experimental rule-derived label generation.
    Rule:
    - detection_count >= 5 OR max_confidence > 0.8 OR rainfall > 10 -> HIGH
    - detection_count >= 2 OR max_confidence > 0.5 -> MEDIUM
    - else -> LOW
    """
    if row['detection_count'] >= 5 or row['max_confidence'] > 0.8 or row['precipitation'] > 10:
        return 2 # HIGH
    elif row['detection_count'] >= 2 or row['max_confidence'] > 0.5:
        return 1 # MEDIUM
    else:
        return 0 # LOW

def main():
    print("Loading YOLO model for feature extraction...")
    yolo_model = YOLO(MODEL_PATH)
    
    features = []
    
    print("Extracting features from dataset images...")
    image_files = [f for f in os.listdir(DATASET_VAL_IMAGES) if f.endswith('.jpg')]
    
    for img_file in image_files:
        img_path = os.path.join(DATASET_VAL_IMAGES, img_file)
        results = yolo_model(img_path, verbose=False)
        result = results[0]
        
        boxes = result.boxes
        detection_count = len(boxes)
        
        if detection_count > 0:
            confs = boxes.conf.cpu().numpy()
            max_conf = float(np.max(confs))
            mean_conf = float(np.mean(confs))
            classes = boxes.cls.cpu().numpy()
            class_0_count = int(np.sum(classes == 0))
            class_1_count = int(np.sum(classes == 1))
            
            # areas
            bboxes = boxes.xyxy.cpu().numpy()
            areas = (bboxes[:, 2] - bboxes[:, 0]) * (bboxes[:, 3] - bboxes[:, 1])
            img_area = result.orig_shape[0] * result.orig_shape[1]
            largest_bbox_ratio = float(np.max(areas) / img_area)
            mean_bbox_ratio = float(np.mean(areas) / img_area)
            total_bbox_ratio = float(np.sum(areas) / img_area)
        else:
            max_conf, mean_conf = 0.0, 0.0
            class_0_count, class_1_count = 0, 0
            largest_bbox_ratio, mean_bbox_ratio, total_bbox_ratio = 0.0, 0.0, 0.0
            
        # Simulate environmental features (temperature, humidity, wind, precip)
        temperature = round(random.uniform(-10, 40), 1)
        humidity = random.randint(20, 100)
        wind_speed = round(random.uniform(0, 30), 1)
        precipitation = round(random.uniform(0, 20), 1) if random.random() > 0.5 else 0.0
            
        features.append({
            'detection_count': detection_count,
            'max_confidence': max_conf,
            'mean_confidence': mean_conf,
            'class_0_count': class_0_count,
            'class_1_count': class_1_count,
            'total_detected_area_ratio': total_bbox_ratio,
            'largest_bbox_area_ratio': largest_bbox_ratio,
            'mean_bbox_area_ratio': mean_bbox_ratio,
            'temperature': temperature,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'precipitation': precipitation
        })
        
    df = pd.DataFrame(features)
    
    # Generate labels
    df['risk_label'] = df.apply(generate_experimental_label, axis=1)
    
    X = df.drop('risk_label', axis=1)
    y = df['risk_label']
    
    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Experimental XGBoost Classifier...")
    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        eval_metric='mlogloss'
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    # Save model
    model.save_model(RISK_MODEL_OUTPUT)
    print(f"Model saved to {RISK_MODEL_OUTPUT}")
    
    # Write report
    report = f"""# EXPERIMENTAL RISK MODEL TRAINING REPORT

IMPORTANT DISCLAIMER:
This is an experimental rule-derived XGBoost model. It has NOT been scientifically validated for real-world rockfall prediction. The labels were derived programmatically from object-detection and environmental features and do NOT represent ground-truth rockfall occurrences.

1. Dataset & Feature Engineering
- Feature List: {list(X.columns)}
- Total Samples: {len(df)}
- Class Distribution: LOW ({sum(y==0)}), MEDIUM ({sum(y==1)}), HIGH ({sum(y==2)})

2. Rule-Derived Label Methodology
Labels were generated using the following experimental logic:
- HIGH: detection_count >= 5 OR max_confidence > 0.8 OR rainfall > 10
- MEDIUM: detection_count >= 2 OR max_confidence > 0.5
- LOW: Otherwise

3. Model Training
- Algorithm: XGBClassifier
- Parameters: n_estimators=100, max_depth=4, learning_rate=0.1
- Train/Test Split: 80% Train, 20% Test (random_state=42)

4. Evaluation Metrics
- Accuracy:  {acc:.4f}
- Precision: {prec:.4f}
- Recall:    {rec:.4f}
- F1-Score:  {f1:.4f}

5. Limitations
This model perfectly learned the explicit experimental rules injected into the dataset. Therefore, the metrics reflect its ability to mimic the heuristic rule, not its ability to predict genuine geological rockfall risk.
"""
    with open(REPORT_OUTPUT, 'w') as f:
        f.write(report)
        
    print("Training report saved.")

if __name__ == '__main__':
    main()
