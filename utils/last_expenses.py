from typing import List, NamedTuple, Optional
from db.db import get_cursor

from utils.user_id_tg import Users_id_tg

class Expense(NamedTuple):
    """Структура добавленного в БД нового расхода"""
    id: Optional[int]
    amount: int
    category_name: str


def last(user_id: int) -> List[Expense]:
    """Возвращает последние несколько расходов"""
    user_id_tg = Users_id_tg().get_user_by_telegram_id(user_id)
    cursor = get_cursor()
    query = """
    SELECT e.id, e.amount, c.name 
    FROM expense e 
    LEFT JOIN category c ON c.codename = e.category_codename 
    WHERE telegram_user_id =?
    ORDER BY created DESC 
    LIMIT 10
    """
    cursor.execute(query, (user_id_tg,))
    rows = cursor.fetchall()
    last_expenses = [Expense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]
    return last_expenses