# ROCKGUARD AI: Smart Rockfall Risk Prediction & Alert System

An end-to-end AI system designed for real-time rockfall hazard assessment and bench stability monitoring in open-pit mines. Combining custom-trained YOLOv11 deep learning computer vision, weather telemetry, and explainable machine learning (XGBoost + SHAP).

---

## 🌟 Key Features

- **YOLOv11 Object Detection**: Custom-trained neural network (`best.pt`) optimized for open-pit mining environments, detecting potential geological shifts, loose debris, and bench irregularities.
- **Explainable Risk Assessment**: XGBoost gradient-boosted decision trees paired with TreeSHAP explanations providing transparent risk scoring (LOW, MEDIUM, HIGH).
- **Interactive Web Dashboard**: High-performance UI built with Vanilla JavaScript, modern glassmorphic aesthetics, and real-time interactive mapping (Leaflet).
- **Dataset Simulation Mode**: Built-in test bench allowing rapid sequential testing across high-resolution mine benchmark imagery.
- **PostgreSQL Database Storage**: Production-grade persistent relational storage recording detection history, bounding boxes, confidence logs, and weather telemetry.

---

## 🏗️ Architecture

```
AI ROCKFALL RISK PREDICTION SYSTEM/
├── backend/
│   ├── main.py                     # FastAPI application & REST endpoints
│   ├── database.py                 # PostgreSQL connection & SQLAlchemy ORM
│   ├── services/
│   │   ├── yolo_service.py         # YOLOv11 model inference pipeline
│   │   ├── risk_service.py         # XGBoost & SHAP risk calculation
│   │   └── weather_service.py      # Telemetry & OpenWeather integration
│   ├── models/                     # XGBoost model definitions
│   ├── runs/                       # Trained YOLOv11 weights (best.pt)
│   └── requirements.txt            # Python dependencies
├── frontend/
│   ├── index.html                  # Responsive UI layout
│   ├── css/
│   │   ├── style.css               # Design system & dark/light theme
│   │   └── login.css               # Authentication modal styling
│   └── js/
│       └── app.js                  # Frontend controllers & state management
└── README.md
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.11+
- PostgreSQL

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Environment Configuration
Copy `.env.example` to `.env` in the `backend/` directory:
```bash
cp .env.example .env
```
Update database connection credentials with your PostgreSQL instance.

### 3. Run Application
```bash
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
Open your browser and navigate to:
- **Application Web UI:** [http://localhost:8000](http://localhost:8000)
- **API Documentation (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

---

## 📊 Model Specifications

| Component | Model / Engine | Metric / Purpose |
| :--- | :--- | :--- |
| **Object Detection** | YOLOv11n (`best.pt`) | 79.1% Precision |
| **Risk Classifier** | XGBoost | Multi-tier hazard assessment |
| **Explainability** | TreeSHAP | Feature importance breakdown per detection |
| **Backend API** | FastAPI / Uvicorn | Async REST Services |
| **Database** | PostgreSQL | Audit trail & historical telemetry |

---

## 📄 License
This project is licensed under the MIT License.
