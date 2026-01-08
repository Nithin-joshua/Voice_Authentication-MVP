import psycopg2
import numpy as np
import os
import uuid

def get_connection():
    database_url = os.getenv("POSTGRES_URL")
    if not database_url:
        raise RuntimeError("POSTGRES_URL not set")
    return psycopg2.connect(database_url)

def save_user(name, email, mean_vector, std_vector):
    user_id = str(uuid.uuid4())

    combined = np.concatenate([mean_vector, std_vector])

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (id, name, email, voice_features)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (email)
        DO UPDATE SET voice_features = EXCLUDED.voice_features
        RETURNING id
    """, (user_id, name, email, psycopg2.Binary(combined.tobytes())))

    saved_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return saved_id

def load_voice_by_email(email):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, voice_features, is_active
        FROM users WHERE email = %s
    """, (email,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        user_id, data, is_active = row
        vec = np.frombuffer(data, dtype=np.float32)
        half = vec.shape[0] // 2
        mean_vector = vec[:half]
        std_vector = vec[half:]
        return user_id, mean_vector, std_vector, is_active

    return None, None, None, None

