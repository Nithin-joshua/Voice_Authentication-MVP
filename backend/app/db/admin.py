import psycopg2
import os

def get_connection():
    return psycopg2.connect(os.getenv("POSTGRES_URL"))


def get_admin_by_email(email: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT email, password_hash FROM admins WHERE email = %s",
        (email,)
    )
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "email": row[0],
        "password_hash": row[1]
    }
