import sqlite3

DATABASE_FILE = "user_database.db"

def create_connection():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        return conn
    except sqlite3.Error as e:
        print(e)
        return None

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        print("Table created successfully")
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def insert_user(conn, email, password):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        print("User inserted successfully.")
    except sqlite3.IntegrityError:
        print("Email already exists. Please choose another email.")
    except sqlite3.Error as e:
        print(e)

if __name__ == "__main__":
    conn = create_connection()
    if conn:
        create_table(conn)
        conn.close()
