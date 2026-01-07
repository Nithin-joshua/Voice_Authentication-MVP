import psycopg2
import numpy as np
import os
import uuid

def get_connection():
    database_url = os.getenv("POSTGRES_URL")
    if not database_url:
        raise RuntimeError("POSTGRES_URL not set")
    return psycopg2.connect(database_url)

def save_user(name, email, features):
    user_id = str(uuid.uuid4())

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (id, name, email, voice_features)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (email)
        DO UPDATE SET voice_features = EXCLUDED.voice_features
        RETURNING id
    """, (user_id, name, email, psycopg2.Binary(features.tobytes())))

    saved_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return saved_id

def load_voice_by_email(email):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, voice_features FROM users WHERE email = %s
    """, (email,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        user_id, data = row
        return user_id, np.frombuffer(data, dtype=np.float32)

    return None, None
