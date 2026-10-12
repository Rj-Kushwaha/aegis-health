import hashlib
import sqlite3

from aegis.database import get_connection


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def create_user(username, email, password, age=None, height=None, weight=None, bmi=None, 
               user_type='patient', medical_id=None, specialization=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO users (username, email, password_hash, age, height, weight, bmi, 
               user_type, medical_id, specialization) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (username, email, hash_password(password), age, height, weight, bmi, 
             user_type, medical_id, specialization)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, username, email, password_hash, user_type, medical_id, specialization FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    
    if user and verify_password(password, user[3]):
        return {
            "id": user[0], 
            "username": user[1], 
            "email": user[2], 
            "user_type": user[4],
            "medical_id": user[5],
            "specialization": user[6]
        }
    return None
