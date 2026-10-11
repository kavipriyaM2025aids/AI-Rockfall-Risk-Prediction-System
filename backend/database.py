import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Local backup reference for SQLite (Not used for production runtime automatically)
SQLITE_DATABASE_URL = "sqlite:///./rockfall.db"

engine = None
SessionLocal = None
POSTGRES_CONFIGURED = False
DB_ENGINE_NAME = "None"

if DB_USER and DB_PASSWORD and DB_HOST and DB_PORT and DB_NAME:
    encoded_password = urllib.parse.quote_plus(DB_PASSWORD)
    SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    POSTGRES_CONFIGURED = True
    DB_ENGINE_NAME = "PostgreSQL"
else:
    print("PostgreSQL configuration is missing. Please set DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME in .env.")

Base = declarative_base()

class PredictionHistory(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    detected_classes = Column(String)  # JSON string of detected classes
    confidence = Column(String)        # JSON string of confidences
    bounding_boxes = Column(String)    # JSON string of bounding boxes
    model_version = Column(String)
    source = Column(String)            # "Dataset" or "User Uploaded Sample"
    risk_status = Column(String, default="NOT_AVAILABLE")
    experimental_flag = Column(String, default="True")
    features_json = Column(String)
    shap_json = Column(String)
    weather_json = Column(String)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    location_name = Column(String, nullable=True)

if POSTGRES_CONFIGURED and engine:
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Failed to create tables in PostgreSQL: {e}")
