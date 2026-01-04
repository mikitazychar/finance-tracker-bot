import sqlite3

DATABASE_NAME = 'finance_bot.db'


def init_db():
    """Инициализация таблиц"""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                income REAL DEFAULT 0
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                category TEXT,
                amount REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()


def set_user_income(user_id: int, income: float):
    """Запись или обновление дохода"""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cur = conn.cursor()
        cur.execute('INSERT OR REPLACE INTO users (user_id, income) VALUES (?, ?)',
                    (user_id, income))
        conn.commit()


def add_expense(user_id: int, category: str, amount: float):
    """Добавление расхода"""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO expenses (user_id, category, amount) VALUES (?, ?, ?)',
                    (user_id, category, amount))
        conn.commit()


def get_user_stats(user_id: int):
    """
    Возвращает кортеж (доход, список трат, общая сумма трат).
    Если данных нет, возвращает 0 и пустые списки.
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cur = conn.cursor()

        cur.execute('SELECT income FROM users WHERE user_id = ?', (user_id,))
        row = cur.fetchone()
        income = row[0] if row else 0.0

        cur.execute('SELECT category, amount FROM expenses WHERE user_id = ? ORDER BY timestamp DESC',
                    (user_id,))
        expenses = cur.fetchall()

        total_spent = sum(item[1] for item in expenses)

        return income, expenses, total_spent


def delete_last_expense(user_id: int):
    """Дополнительная полезная функция: удаление последней записи пользователя"""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cur = conn.cursor()
        cur.execute('''
            DELETE FROM expenses
            WHERE id = (SELECT MAX(id) FROM expenses WHERE user_id = ?)
        ''', (user_id,))
        conn.commit()
