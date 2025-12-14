import sqlite3
from typing import List, Dict, Any
from datetime import datetime

DB_NAME = "finance.db"

def init_db():
    """Initializes the database table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_transaction(description: str, amount: float, category: str):
    """Saves a transaction to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO transactions (description, amount, category, date) VALUES (?, ?, ?, ?)',
                   (description, amount, category, date_str))
    conn.commit()
    conn.close()

def get_recent_transactions(limit: int = 5) -> List[Dict[str, Any]]:
    """Fetches the N most recent transactions."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions ORDER BY id DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_transactions() -> List[Dict[str, Any]]:
    """Fetches all transactions for the ledger."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_daily_spending() -> Dict[str, float]:
    """Calculates spending grouped by date (YYYY-MM-DD) for the last 7 active days."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Extract YYYY-MM-DD
    cursor.execute('SELECT substr(date, 1, 10) as day, SUM(amount) FROM transactions GROUP BY day ORDER BY day ASC LIMIT 10')
    rows = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}

def get_category_summary() -> Dict[str, float]:
    """Calculates total spending per category."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT category, SUM(amount) FROM transactions GROUP BY category')
    rows = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}
