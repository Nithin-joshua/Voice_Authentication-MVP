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

def get_all_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, email, created_at, is_active
        FROM users
        ORDER BY created_at DESC
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    users = []
    for row in rows:
        users.append({
            "id": str(row[0]),
            "name": row[1],
            "email": row[2],
            "created_at": row[3],
            "is_active": row[4]
        })

    return users
def set_user_status(user_id: str, is_active: bool):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET is_active = %s WHERE id = %s",
        (is_active, user_id)
    )

    conn.commit()
    cur.close()
    conn.close()
