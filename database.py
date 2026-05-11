import sqlite3, json, hashlib, os
from datetime import datetime

DB_PATH = 'loan_predictions.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            username      TEXT UNIQUE NOT NULL,
            email         TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin      INTEGER DEFAULT 0,
            created_at    TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id        INTEGER,
            applicant_name TEXT,
            age            INTEGER,
            gender         TEXT,
            income         REAL,
            loan_amount    REAL,
            loan_term      INTEGER,
            cibil_score    INTEGER,
            credit_history INTEGER,
            employment     TEXT,
            education      TEXT,
            property_area  TEXT,
            result         TEXT,
            probability    REAL,
            input_data     TEXT,
            created_at     TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    # Create default admin if none exists
    c.execute("SELECT COUNT(*) FROM users WHERE is_admin=1")
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO users (name, username, email, password_hash, is_admin, created_at)
            VALUES (?,?,?,?,?,?)
        ''', ('Administrator', 'admin', 'admin@loanapp.com',
              hash_password('admin123'), 1,
              datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def create_user(name, username, email, password):
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (name, username, email, password_hash, is_admin, created_at)
        VALUES (?,?,?,?,0,?)
    ''', (name, username, email, hash_password(password),
          datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def is_admin(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT is_admin FROM users WHERE id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return bool(row and row['is_admin'])

def get_all_users():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT u.id, u.name, u.username, u.email, u.is_admin, u.created_at,
               COUNT(p.id) as total_predictions
        FROM users u
        LEFT JOIN predictions p ON p.user_id = u.id
        GROUP BY u.id ORDER BY u.created_at DESC
    ''')
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def delete_user(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM predictions WHERE user_id=?", (user_id,))
    c.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

def save_prediction(input_data: dict, result: dict):
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO predictions
        (user_id, applicant_name, age, gender, income, loan_amount, loan_term,
         cibil_score, credit_history, employment, education, property_area,
         result, probability, input_data, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (
        input_data.get('user_id'),
        input_data.get('name', 'Unknown'),
        input_data.get('age', 0),
        input_data.get('gender', ''),
        input_data.get('income', 0),
        input_data.get('lamt', 0),
        input_data.get('lterm', 360),
        input_data.get('cibil', 0),
        input_data.get('ch', 0),
        input_data.get('emp', ''),
        input_data.get('edu', ''),
        input_data.get('prop', ''),
        result.get('label', ''),
        result.get('probability', 0),
        json.dumps(input_data),
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))
    conn.commit()
    conn.close()

def get_history(limit=50, user_id=None):
    conn = get_db()
    c = conn.cursor()
    if user_id:
        c.execute('''SELECT p.id, p.applicant_name, p.income, p.loan_amount,
                     p.cibil_score, p.result, p.probability, p.created_at,
                     u.username
                     FROM predictions p
                     LEFT JOIN users u ON u.id = p.user_id
                     WHERE p.user_id=? ORDER BY p.created_at DESC LIMIT ?''', (user_id, limit))
    else:
        c.execute('''SELECT p.id, p.applicant_name, p.income, p.loan_amount,
                     p.cibil_score, p.result, p.probability, p.created_at,
                     u.username
                     FROM predictions p
                     LEFT JOIN users u ON u.id = p.user_id
                     ORDER BY p.created_at DESC LIMIT ?''', (limit,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_stats(user_id=None):
    conn = get_db()
    c = conn.cursor()
    where = "WHERE user_id=?" if user_id else ""
    params = (user_id,) if user_id else ()
    c.execute(f"SELECT COUNT(*) FROM predictions {where}", params)
    total = c.fetchone()[0]
    c.execute(f"SELECT COUNT(*) FROM predictions {where} {'AND' if user_id else 'WHERE'} result='Approved'" if user_id else f"SELECT COUNT(*) FROM predictions WHERE result='Approved'", params if user_id else ())
    approved = c.fetchone()[0]
    c.execute(f"SELECT AVG(probability) FROM predictions {where}", params)
    avg_prob = c.fetchone()[0] or 0
    conn.close()
    return {
        'total': total, 'approved': approved,
        'rejected': total - approved,
        'approval_rate': round((approved / total * 100) if total else 0, 1),
        'avg_probability': round(avg_prob, 1)
    }