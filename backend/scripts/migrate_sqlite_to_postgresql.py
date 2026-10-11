import os
import sys
import sqlite3
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import urllib.parse

# Append parent dir to access database.py models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import PredictionHistory, Base

load_dotenv()

def migrate():
    sqlite_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rockfall.db")
    if not os.path.exists(sqlite_path):
        print(f"SQLite database not found at {sqlite_path}. Nothing to migrate.")
        return

    print(f"Reading from SQLite database: {sqlite_path}")
    sqlite_conn = sqlite3.connect(sqlite_path)
    sqlite_cursor = sqlite_conn.cursor()

    try:
        sqlite_cursor.execute("SELECT id, image_name, timestamp, detected_classes, confidence, bounding_boxes, model_version, source FROM predictions")
        records = sqlite_cursor.fetchall()
    except Exception as e:
        print(f"Error reading from SQLite: {e}")
        return
        
    if not records:
        print("No records found in SQLite to migrate.")
        return
        
    print(f"Found {len(records)} records in SQLite.")

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
        print("PostgreSQL configuration is incomplete. Please set DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME in .env.")
        print("Migration aborted safely.")
        return

    encoded_password = urllib.parse.quote_plus(DB_PASSWORD)
    postgres_url = f"postgresql+psycopg2://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    try:
        engine = create_engine(postgres_url)
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return

    migrated_count = 0
    skipped_count = 0

    try:
        for row in records:
            p_id, image_name, timestamp_raw, detected_classes, confidence, bounding_boxes, model_version, source = row
            
            existing = session.query(PredictionHistory).filter(PredictionHistory.id == p_id).first()
            if existing:
                skipped_count += 1
                continue
                
            parsed_timestamp = datetime.utcnow()
            if isinstance(timestamp_raw, str):
                try:
                    parsed_timestamp = datetime.strptime(timestamp_raw.split(".")[0], "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    pass
            elif isinstance(timestamp_raw, datetime):
                parsed_timestamp = timestamp_raw
                
            new_record = PredictionHistory(
                id=p_id,
                image_name=image_name,
                timestamp=parsed_timestamp,
                detected_classes=detected_classes,
                confidence=confidence,
                bounding_boxes=bounding_boxes,
                model_version=model_version,
                source=source
            )
            session.add(new_record)
            migrated_count += 1
            
        session.commit()
        print(f"Migration completed successfully.")
        print(f"Migrated: {migrated_count} records.")
        print(f"Skipped (already exists in PostgreSQL): {skipped_count} records.")
    except Exception as e:
        session.rollback()
        print(f"Migration failed during transfer. Rolled back PostgreSQL changes. Error: {e}")
    finally:
        session.close()
        sqlite_conn.close()

if __name__ == "__main__":
    migrate()
