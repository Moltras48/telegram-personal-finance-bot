from db.db import get_cursor

from utils.user_id_tg import Users_id_tg

def upload_data_db(user_id: int) -> str:
    """Возвращает строкой статистику расходов за сегодня"""
    user_id_tg = Users_id_tg().get_user_by_telegram_id(user_id)
    cursor = get_cursor()
    query = "SELECT * FROM expense WHERE telegram_user_id =?"
    cursor.execute(query, (user_id_tg,))
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    
    return columns, rows