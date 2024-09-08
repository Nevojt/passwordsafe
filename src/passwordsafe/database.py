import sqlite3
import toga


# Функція для створення таблиці в базі даних
def create_table(conn):
    """Створення таблиці для зберігання паролів у базі даних"""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()


# Функція для збереження пароля в базу даних
def save_password_to_db(conn, url, password):
    """Зберігаємо пароль у базу даних"""
    if url and password:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO passwords (url, password) VALUES (?, ?)', (url, password))
        conn.commit()

        return True
    else:
        return False
