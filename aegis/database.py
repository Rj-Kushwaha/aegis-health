import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "data" / "medical_app.db"
LEGACY_DB_PATH = ROOT_DIR / "medical_app.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if LEGACY_DB_PATH.exists() and not DB_PATH.exists():
        LEGACY_DB_PATH.replace(DB_PATH)
    return sqlite3.connect(DB_PATH)


def adapt_datetime(value):
    return value.strftime("%Y-%m-%d %H:%M:%S")


sqlite3.register_adapter(datetime, adapt_datetime)


def save_consultation(user_id, symptoms, diagnosis, recommendations, severity):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO consultations (user_id, symptoms, diagnosis, recommendations, severity)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, symptoms, diagnosis, recommendations, severity))
    conn.commit()
    conn.close()

def get_user_consultations(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM consultations WHERE user_id = ? ORDER BY created_at DESC
    ''', (user_id,))
    consultations = cursor.fetchall()
    conn.close()
    return consultations

def init_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table with enhanced fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            age INTEGER,
            height REAL,
            weight REAL,
            bmi REAL,
            user_type TEXT DEFAULT 'patient',
            medical_id TEXT,
            specialization TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Consultations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            symptoms TEXT,
            diagnosis TEXT,
            recommendations TEXT,
            severity TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Medicine reminders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicine_reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            medicine_name TEXT NOT NULL,
            dosage TEXT,
            frequency TEXT,
            time_slots TEXT,
            start_date DATE,
            end_date DATE,
            active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Notifications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            message TEXT,
            scheduled_time TIMESTAMP,
            sent BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_medicine_reminder(user_id, medicine_name, dosage, frequency, time_slots, start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """INSERT INTO medicine_reminders (user_id, medicine_name, dosage, frequency, 
           time_slots, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (user_id, medicine_name, dosage, frequency, json.dumps(time_slots), start_date, end_date)
    )
    conn.commit()
    conn.close()

def get_user_reminders(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM medicine_reminders WHERE user_id = ? AND active = TRUE ORDER BY created_at DESC",
        (user_id,)
    )
    reminders = cursor.fetchall()
    conn.close()
    
    return reminders

def create_water_reminder(user_id, frequency_hours=2):
    """Create daily water reminders"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Clear existing water reminders for today
    today = datetime.now().date()
    cursor.execute(
        "DELETE FROM notifications WHERE user_id = ? AND type = 'water' AND DATE(scheduled_time) = ?",
        (user_id, today)
    )
    
    # Create water reminders every 2 hours from 8 AM to 10 PM
    start_hour = 8
    end_hour = 22
    
    for hour in range(start_hour, end_hour + 1, frequency_hours):
        reminder_time = datetime.combine(today, datetime.min.time().replace(hour=hour))
        cursor.execute(
            """INSERT INTO notifications (user_id, type, message, scheduled_time) 
               VALUES (?, ?, ?, ?)""",
            (user_id, 'water', '💧 Time to drink water! Stay hydrated for better health.', reminder_time)
        )
    
    conn.commit()
    conn.close()


def get_and_mark_due_notifications(user_id, now):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT * FROM notifications
           WHERE user_id = ? AND sent = FALSE AND scheduled_time <= ?
           ORDER BY scheduled_time""",
        (user_id, now),
    )
    notifications = cursor.fetchall()
    for notification in notifications:
        cursor.execute("UPDATE notifications SET sent = TRUE WHERE id = ?", (notification[0],))
    conn.commit()
    conn.close()
    return notifications
