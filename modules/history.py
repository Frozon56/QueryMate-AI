import sqlite3

DB = "history.db"


# ============================================
# CREATE TABLE
# ============================================

def create_history_table():

    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()

    except Exception as e:
        print("Create Table Error:", e)

    finally:
        conn.close()


# ============================================
# SAVE HISTORY
# ============================================

def save_history(username, question, answer):

    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()

        c.execute("""
            INSERT INTO history(username, question, answer)
            VALUES (?, ?, ?)
        """, (username, question, answer))

        conn.commit()

        return True

    except Exception as e:
        print("Save History Error:", e)
        return False

    finally:
        conn.close()


# ============================================
# GET HISTORY
# ============================================

def get_history(username):

    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()

        c.execute("""
            SELECT question, answer, created_at
            FROM history
            WHERE username = ?
            ORDER BY id DESC
        """, (username,))

        rows = c.fetchall()

        return rows

    except Exception as e:
        print("Get History Error:", e)
        return []

    finally:
        conn.close()


# ============================================
# CLEAR HISTORY
# ============================================

def clear_history(username):

    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()

        c.execute("""
            DELETE FROM history
            WHERE username = ?
        """, (username,))

        conn.commit()

        return True

    except Exception as e:
        print("Clear History Error:", e)
        return False

    finally:
        conn.close()