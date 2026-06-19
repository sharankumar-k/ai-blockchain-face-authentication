import psycopg2
import pickle

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "sharan"
DB_HOST = "localhost"
DB_PORT = "5432"


# -----------------------------------
# Database Connection
# -----------------------------------
def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


# -----------------------------------
# Initialize database
# -----------------------------------
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email VARCHAR(255) PRIMARY KEY,
            password TEXT NOT NULL,
            embedding BYTEA,
            face_hash TEXT NOT NULL
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


# -----------------------------------
# Check if user exists
# -----------------------------------
def user_exists(email):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM users WHERE email=%s LIMIT 1",
        (email,)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    return row is not None


# -----------------------------------
# Store new user
# -----------------------------------
def store_user(email, password, embedding, face_hash):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO users
        (email, password, embedding, face_hash)
        VALUES (%s, %s, %s, %s)
        """,
        (
            email,
            password,
            pickle.dumps(embedding),
            face_hash
        )
    )

    conn.commit()

    cur.close()
    conn.close()


# -----------------------------------
# Fetch stored password + embedding + hash
# -----------------------------------
def get_user(email):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT password, embedding, face_hash
        FROM users
        WHERE email=%s
        """,
        (email,)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        password = row[0]
        embedding = pickle.loads(row[1])
        face_hash = row[2]

        return password, embedding, face_hash

    return None, None, None