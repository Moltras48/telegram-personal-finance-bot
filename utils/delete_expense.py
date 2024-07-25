from db.db import delete, check_for_delete
from utils.user_id_tg import Users_id_tg

def delete_expense(row_id: int, user_id: int) -> None:
    """Удаляет сообщение по его идентификатору"""
    user_id_tg = Users_id_tg().get_user_by_telegram_id(user_id)
    check = check_for_delete("expense", row_id, user_id_tg)
    if len(check) != 0:
        delete("expense", row_id, user_id_tg)
        text_delete = 'Запись успешно удалена!'
    else:
        text_delete = 'Нельзя удалить чужую запись!'
    return text_delete