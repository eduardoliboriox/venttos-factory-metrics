from app.extensions import get_db
from psycopg.rows import dict_row

def get_user_by_provider(provider, provider_id):
    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
              SELECT * FROM users
              WHERE provider=%s AND provider_id=%s
            """, (provider, provider_id))
            return cur.fetchone()

def create_user(data):
    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
              INSERT INTO users (username, email, provider, provider_id)
              VALUES (%s,%s,%s,%s)
              RETURNING *
            """, (
                data["username"],
                data["email"],
                data["provider"],
                data["provider_id"]
            ))
            conn.commit()
            return cur.fetchone()

def get_user_by_id(user_id):
    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
            return cur.fetchone()
