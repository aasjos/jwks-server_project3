import sqlite3

def init_db():
    conn = sqlite3.connect('totally_not_my_privateKeys.db')
    c = conn.cursor()

    # Create the necessary tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE,
            date_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        );
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS auth_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_ip TEXT NOT NULL,
            request_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS keys (
            kid INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL,
            exp INTEGER
        );
    ''')

    conn.commit()
    conn.close()
    print("✅ Database and tables created!")

if __name__ == '__main__':
    init_db()
