import os
import json
import xgboost as xgb
import shap
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'risk_xgboost.json')

_model = None
_explainer = None

def load_model():
    global _model, _explainer
    if _model is None:
        try:
            if os.path.exists(MODEL_PATH):
                _model = xgb.XGBClassifier()
                _model.load_model(MODEL_PATH)
                _explainer = shap.TreeExplainer(_model)
        except Exception as e:
            print(f"Error loading XGBoost model: {e}")

def assess_risk(yolo_result, weather_data=None):
    load_model()
    
    # Feature extraction exactly as trained
    detections = yolo_result.get("detections", [])
    detection_count = len(detections)
    
    if detection_count > 0:
        confs = [d["confidence"] for d in detections]
        max_conf = max(confs)
        mean_conf = sum(confs) / len(confs)
        class_0_count = sum(1 for d in detections if d["class_id"] == 0)
        class_1_count = sum(1 for d in detections if d["class_id"] == 1)
        
        img_w = yolo_result.get("image_width", 1024)
        img_h = yolo_result.get("image_height", 1024)
        img_area = img_w * img_h
        
        areas = []
        for d in detections:
            bbox = d.get("bbox", {})
            if bbox:
                areas.append((bbox["x2"] - bbox["x1"]) * (bbox["y2"] - bbox["y1"]))
                
        if areas:
            largest_bbox_ratio = max(areas) / img_area
            mean_bbox_ratio = sum(areas) / len(areas) / img_area
            total_bbox_ratio = sum(areas) / img_area
        else:
            largest_bbox_ratio, mean_bbox_ratio, total_bbox_ratio = 0.0, 0.0, 0.0
    else:
        max_conf, mean_conf = 0.0, 0.0
        class_0_count, class_1_count = 0, 0
        largest_bbox_ratio, mean_bbox_ratio, total_bbox_ratio = 0.0, 0.0, 0.0
        
    weather = weather_data or {}
    temperature = weather.get("temperature", 20.0)
    humidity = weather.get("humidity", 50.0)
    wind_speed = weather.get("wind_speed", 5.0)
    # Check if 'precipitation' is provided directly or mapped from OWM structure
    precipitation = weather.get("precipitation", 0.0)
    if 'rain' in weather and type(weather['rain']) is dict:
        precipitation = weather['rain'].get('1h', 0.0)
        
    features_dict = {
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
    }
    
    df = pd.DataFrame([features_dict])
    
    if _model is None:
        # Fallback if model not trained yet
        return {
            "risk_level": "NOT_AVAILABLE",
            "model": "None",
            "experimental": True,
            "validated": False,
            "features": features_dict,
            "shap_explanation": []
        }
        
    # Predict
    pred = _model.predict(df)[0]
    risk_mapping = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}
    risk_level = risk_mapping.get(int(pred), "NOT_AVAILABLE")
    
    # SHAP
    shap_explanation = []
    if _explainer:
        try:
            shap_values = _explainer.shap_values(df)
            # shap_values could be a list for multi-class classification
            # XGBoost multi-class returns list of length n_classes
            if isinstance(shap_values, list):
                class_shap = shap_values[int(pred)][0]
            else:
                class_shap = shap_values[0]
                
            # Get top 3 features by absolute SHAP value
            feature_names = df.columns
            contribs = [(feature_names[i], float(class_shap[i])) for i in range(len(feature_names))]
            contribs.sort(key=lambda x: abs(x[1]), reverse=True)
            
            for feat, val in contribs[:4]:
                if abs(val) > 0.001:
                    shap_explanation.append({
                        "feature": feat,
                        "contribution": val,
                        "value": float(features_dict[feat])
                    })
        except Exception as e:
            print(f"SHAP Error: {e}")
            
    return {
        "risk_level": risk_level,
        "model": "XGBoost",
        "experimental": True,
        "validated": False,
        "features": features_dict,
        "shap_explanation": shap_explanation
    }
