import sqlite3

DB_PATH = r'C:\AI_DEV\AgentSwarm\n8n_data\database.sqlite'

def check_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    print("Tables in database:")
    for t in sorted(tables):
        print(f"  - {t}")
    conn.close()

if __name__ == "__main__":
    check_tables()
