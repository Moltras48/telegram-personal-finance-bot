import os
from typing import Dict, List, Optional

import sqlite3

# Подключение к базе данных
DATABASE_PATH = os.path.join("/telegram-personal-finance-bot/db", "finance.db")
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

def insert(table: str, column_values: Dict) -> None:
    """
    Вставляет данные в указанную таблицу.
    
    :param table: Название таблицы.
    :param column_values: Словарь с данными для вставки.
    """
    placeholders = ", ".join("?" * len(column_values))
    columns = ', '.join(column_values.keys())
    values = tuple(column_values.values())
    query = f"INSERT INTO {table} ({columns }) VALUES ({placeholders})" # WHERE {user_id} = 1
    cursor.execute(query, values)  # Передача кортежа значений напрямую
    conn.commit()
    
def add_users(user_id: int) -> None:
    """
    Вставляет user_id telegram в таблицу users.   
    
    :user_id: Айдти юзера в телеграме.
    """
    cursor.execute("SELECT COUNT(*) FROM users WHERE telegram_id=?", (user_id,))
    count = cursor.fetchone()[0]
    
    if count == 0:
        query = "INSERT INTO users (telegram_id) VALUES (?)"
        cursor.execute(query, (user_id,))
        conn.commit()

def fetchall(table: str, columns: List[str]) -> List[Dict]:
    """
    Извлекает все строки из указанной таблицы.
    
    :param table: Название таблицы.
    :param columns: Список столбцов для выборки.
    :return: Список словарей с данными.
    """
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    return [{column: value for column, value in zip(columns, row)} for row in rows]

def fetchall_where(table: str, columns: List[str], user_tg_id: int) -> List[Dict]:
    """
    Извлекает все строки из указанной таблицы.
    
    :param table: Название таблицы.
    :param columns: Список столбцов для выборки.
    :return: Список словарей с данными.
    """
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table} WHERE telegram_user_id={user_tg_id}")
    rows = cursor.fetchall()
    return [{column: value for column, value in zip(columns, row)} for row in rows]

def check_for_delete(table: str, row_id: int, user_id_tg: int):
    """
    Проверяет есть ли в базе данных такая новость с таким же айди юзера тг.
    
    :param table: Название таблицы.
    :param row_id: ID удаляемой строки.
    :param user_id_tg: ID пользователя телеграма в БД.
    """
    query = f"SELECT * FROM {table} WHERE id={row_id} AND telegram_user_id={user_id_tg}"
    cursor.execute(query)
    conn.commit()
    rows = cursor.fetchall()
    return rows

def delete(table: str, row_id: int, user_id_tg: int) -> None:
    """
    Удаляет строку по ID из указанной таблицы.
    
    :param table: Название таблицы.
    :param row_id: ID удаляемой строки.
    :param user_id_tg: ID пользователя телеграма в БД.
    """
    query = f"DELETE FROM {table} WHERE id={row_id} AND telegram_user_id={user_id_tg}"
    cursor.execute(query)
    conn.commit()
 
def add_user_daily_limit(user_id_tg: int) -> None:
    """
    Устанавливает ежедневный лимит в 100 по умолчанию для нового юзера.
    
    :param new_limit: Новый лимит.
    :param user_id_tg: ID пользователя телеграма в БД.
    """
    cursor.execute("SELECT COUNT(*) FROM budget WHERE telegram_user_id=?", (user_id_tg,))
    count = cursor.fetchone()[0]
    
    if count == 0:
        query = f"INSERT INTO budget(codename, daily_limit, telegram_user_id) VALUES ('base', 1000, {user_id_tg})"
        cursor.execute(query)
        conn.commit() 

def check_daily_limit(user_id_tg: int) -> None:
    """
    Обновляет ежедневный лимит для заданного кода.
    
    :param new_limit: Новый лимит.
    :param user_id_tg: ID пользователя телеграма в БД.
    """
    query = f"SELECT daily_limit FROM budget WHERE telegram_user_id={user_id_tg}"
    cursor.execute(query)
    conn.commit()
    rows = cursor.fetchall()
    return rows
 
def update_daily_limit(new_limit: int, user_id_tg: int) -> None:
    """
    Обновляет ежедневный лимит для заданного кода.
    
    :param new_limit: Новый лимит.
    :param user_id_tg: ID пользователя телеграма в БД.
    """
    query = f"UPDATE budget SET daily_limit={new_limit} WHERE telegram_user_id={user_id_tg}"
    cursor.execute(query)
    conn.commit()
    
def get_cursor() -> sqlite3.Cursor:
    """
    Возвращает курсор соединения с базой данных.
    
    :return: Курсор.
    """
    return cursor

def _init_db() -> None:
    """
    Инициализирует базу данных, выполняя SQL-скрипт из файла.
    """
    with open("db/createdb.sql", "r", encoding='utf-8') as file:
        sql_script = file.read()
    cursor.executescript(sql_script)
    conn.commit()

def check_db_exists() -> None:
    """
    Проверяет наличие таблицы 'expense'. Если таблица отсутствует, инициализирует базу данных.
    """
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='expense'")
    table_exists = cursor.fetchone()
    if not table_exists:
        _init_db()

# Вызов функции для проверки и инициализации базы данных
check_db_exists()