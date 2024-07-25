import datetime
from db.db import get_cursor,fetchall_where

from utils.user_id_tg import Users_id_tg

def get_today_statistics(user_id: int) -> str:
    """Возвращает строкой статистику расходов за сегодня"""
    user_id_tg = Users_id_tg().get_user_by_telegram_id(user_id)
    cursor = get_cursor()
    query = "SELECT sum(amount) FROM expense WHERE date(created) = date('now', 'localtime') AND telegram_user_id =?"
    cursor.execute(query, (user_id_tg,))
    result = cursor.fetchone()
    if not result[0]:
        return "Сегодня ещё нет расходов"
    all_today_expenses = result[0]
    query = """
    SELECT sum(amount) 
    FROM expense 
    WHERE date(created) = date('now', 'localtime') 
    AND category_codename IN (
        SELECT codename 
        FROM category 
        WHERE is_base_expense=true
    ) 
    AND telegram_user_id =?
    """
    cursor.execute(query, (user_id_tg,))
    result = cursor.fetchone()
    base_today_expenses = result[0] if result[0] else 0
    query = """
    SELECT date(created) 
    FROM expense 
    WHERE date(created) = date('now', 'localtime') 
    AND category_codename IN (
        SELECT codename 
        FROM category 
        WHERE is_base_expense=true
    ) 
    AND telegram_user_id =?
    """

    cursor.execute(query, (user_id_tg,))
    date = cursor.fetchone()
    if date is None:
        return "Сегодня ещё нет расходов"
    date_today = date[0]
    date_today_format = datetime.datetime.strptime(date_today, "%Y-%m-%d")

    # Преобразуем datetime обратно в date, чтобы избавиться от времени
    date_only = date_today_format.date()

    # Форматируем date в строку без времени
    formatted_date = date_only.strftime("%Y-%m-%d")
    
    return (f"Расходы сегодня ({formatted_date}):\n\n"
            f"Всего потрачено за день — {all_today_expenses} руб.\n\n"
            f"Можно потратить за день — {_get_budget_limit(user_id_tg) -base_today_expenses} руб.\n\n")
    
    
def _get_budget_limit(user_id: int) -> int:
    """Возвращает дневной лимит трат для основных базовых трат"""
    return fetchall_where("budget", ["daily_limit"], user_id)[0]["daily_limit"]