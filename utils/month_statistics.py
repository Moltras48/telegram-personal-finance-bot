import pytz
import datetime
from db.db import get_cursor, fetchall_where
import calendar

from utils.user_id_tg import Users_id_tg

def get_month_statistics(user_id: int) -> str:
    """Возвращает строкой статистику расходов за текущий месяц"""
    user_id_tg = Users_id_tg().get_user_by_telegram_id(user_id)
    now = _get_now_datetime()
    # Извлекаем год и месяц из текущей даты
    year = now.year
    month = now.month

    # Используем monthrange для получения количества дней в текущем месяце
    _, number_of_days = calendar.monthrange(year, month)
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    cursor = get_cursor()
    query = f"""
    SELECT sum(amount) 
    FROM expense 
    WHERE date(created) >= '{first_day_of_month}' 
    AND telegram_user_id =?
    """
    cursor.execute(query, (user_id_tg,))
    result = cursor.fetchone()
    if not result[0]:
        return "В этом месяце ещё нет расходов"
    all_today_expenses = result[0]
    query = f"""
    SELECT sum(amount) 
    FROM expense 
    WHERE date(created) >= '{first_day_of_month}' 
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
    return (f"Расходы в текущем месяце:\n\n"
            f"Всего потрачено за месяц — {all_today_expenses} руб.\n\n"
            f"Можно потратить за месяц —  {(number_of_days * _get_budget_limit(user_id_tg) - base_today_expenses)} руб.")
    
    
def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now

def _get_budget_limit(user_id: int) -> int:
    """Возвращает дневной лимит трат для основных базовых трат"""
    return fetchall_where("budget", ["daily_limit"], user_id)[0]["daily_limit"]