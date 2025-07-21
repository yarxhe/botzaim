# src/database.py
import sqlite3
from datetime import datetime
from . import config

DB_NAME = config.DB_NAME

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS debts
    (user_id INTEGER, creditor TEXT, amount REAL, due_date TEXT, created_at TEXT, PRIMARY KEY (user_id, creditor, created_at))
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS receivables
    (user_id INTEGER, debtor TEXT, amount REAL, due_date TEXT, created_at TEXT, PRIMARY KEY (user_id, debtor, created_at))
    ''')
    conn.commit()
    conn.close()

# --- Функции для 'debts' (Я должен) ---

def add_debt(user_id, creditor, amount, due_date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO debts (user_id, creditor, amount, due_date, created_at) VALUES (?, ?, ?, ?, ?)", (user_id, creditor, float(amount), due_date, created_at))
    conn.commit()
    conn.close()

def get_creditors(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT creditor FROM debts WHERE user_id = ?", (user_id,))
    return [row[0] for row in cursor.fetchall()]

def get_debts_by_creditor(user_id, creditor):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT amount, due_date, created_at FROM debts WHERE user_id = ? AND creditor = ?", (user_id, creditor))
    return cursor.fetchall()

def get_debt_by_id(debt_id):
    user_id, creditor, created_at = debt_id
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT amount, due_date FROM debts WHERE user_id = ? AND creditor = ? AND created_at = ?", (user_id, creditor, created_at))
    return cursor.fetchone()

def update_debt_amount(debt_id, new_amount):
    user_id, creditor, created_at = debt_id
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE debts SET amount = ? WHERE user_id = ? AND creditor = ? AND created_at = ?", (new_amount, user_id, creditor, created_at))
    conn.commit()
    conn.close()

def delete_debt(debt_id):
    user_id, creditor, created_at = debt_id
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM debts WHERE user_id = ? AND creditor = ? AND created_at = ?", (user_id, creditor, created_at))
    conn.commit()
    conn.close()

def get_total_debt(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM debts WHERE user_id = ?", (user_id,))
    total = cursor.fetchone()[0]
    return total if total else 0

def get_debts_due_soon(days_ahead: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, creditor, amount, due_date FROM debts")
    all_debts = cursor.fetchall()
    conn.close()
    
    due_soon_list = []
    today = datetime.now()
    for debt in all_debts:
        user_id, name, amount, due_date_str = debt
        try:
            due_date = datetime.strptime(due_date_str, "%d.%m.%Y")
            delta = (due_date - today).days
            if 0 <= delta <= days_ahead:
                due_soon_list.append({"user_id": user_id, "name": name, "amount": amount, "due_date": due_date_str, "days_left": delta})
        except (ValueError, TypeError):
            continue
    return due_soon_list
    

# --- Функции для 'receivables' (Мне должны) ---

def add_receivable(user_id, debtor, amount, due_date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO receivables (user_id, debtor, amount, due_date, created_at) VALUES (?, ?, ?, ?, ?)", (user_id, debtor, float(amount), due_date, created_at))
    conn.commit()
    conn.close()

def get_debtors(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT debtor FROM receivables WHERE user_id = ?", (user_id,))
    return [row[0] for row in cursor.fetchall()]

def get_receivables_by_debtor(user_id, debtor):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT amount, due_date, created_at FROM receivables WHERE user_id = ? AND debtor = ?", (user_id, debtor))
    return cursor.fetchall()

def get_receivable_by_id(receivable_id):
    user_id, debtor, created_at = receivable_id
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT amount, due_date FROM receivables WHERE user_id = ? AND debtor = ? AND created_at = ?", (user_id, debtor, created_at))
    return cursor.fetchone()

def update_receivable_amount(receivable_id, new_amount):
    user_id, debtor, created_at = receivable_id
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE receivables SET amount = ? WHERE user_id = ? AND debtor = ? AND created_at = ?", (new_amount, user_id, debtor, created_at))
    conn.commit()
    conn.close()

def delete_receivable(receivable_id):
    user_id, debtor, created_at = receivable_id
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM receivables WHERE user_id = ? AND debtor = ? AND created_at = ?", (user_id, debtor, created_at))
    conn.commit()
    conn.close()

def get_total_receivables(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM receivables WHERE user_id = ?", (user_id,))
    total = cursor.fetchone()[0]
    return total if total else 0

def get_receivables_due_soon(days_ahead: int):
    """Ищет долги ВАМ, у которых скоро истекает срок."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Запрос к таблице receivables
    cursor.execute("SELECT user_id, debtor, amount, due_date FROM receivables")
    all_receivables = cursor.fetchall()
    conn.close()
    
    due_soon_list = []
    today = datetime.now()
    for receivable in all_receivables:
        user_id, name, amount, due_date_str = receivable
        try:
            due_date = datetime.strptime(due_date_str, "%d.%m.%Y")
            delta = (due_date - today).days
            if 0 <= delta <= days_ahead:
                due_soon_list.append({
                    "user_id": user_id,
                    "name": name,
                    "amount": amount,
                    "due_date": due_date_str,
                    "days_left": delta
                })
        except (ValueError, TypeError):
            continue
    return due_soon_list