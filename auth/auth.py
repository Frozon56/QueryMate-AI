import sqlite3
import bcrypt


DB = "users.db"

def create_users_table():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password BLOB NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def register_user(username, password):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if c.fetchone():
        conn.close()
        return False

    hashed = hash_password(password)

    c.execute(
        "INSERT INTO users(username,password) VALUES (?,?)",
        (username, hashed)
    )

    conn.commit()
    conn.close()
    return True


def login_user(username, password):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    user = c.fetchone()
    conn.close()

    if user:
        return bcrypt.checkpw(password.encode(), user[0])

    return False