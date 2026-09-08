import sqlite3

My_post = []

users_db = {}


def get_db_connection():
    conn = sqlite3.connect("Mydatabase.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    """Create database tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)
    
    # Create posts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()


# Initialize tables when imported
create_tables()