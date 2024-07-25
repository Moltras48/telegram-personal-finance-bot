from typing import List, NamedTuple, Optional

from db.db import fetchall

class User_id_tg(NamedTuple):
    """Структура таблицы users"""
    id: int
    telegram_id: int

class Users_id_tg:
    def __init__(self):
        self._user_id_tg = self._load_user_ids()

    def _load_user_ids(self) -> List[User_id_tg]:
        """Возвращает список объектов User_id_tg из БД"""
        user_ids = fetchall("users", ["id", "telegram_id"])
        # Преобразование списка словарей в список объектов User_id_tg
        user_ids = [User_id_tg(id=row['id'], telegram_id=row['telegram_id']) for row in user_ids]
        return user_ids

    def get_all_users(self) -> List[User_id_tg]:
        """Возвращает список всех пользователей."""
        return self._user_id_tg
    
    def get_user_by_telegram_id(self, telegram_id: int) -> Optional[int]:
        """Возвращает ID пользователя В БД по его ID в Telegram, иначе None."""
        for user in self._user_id_tg:
            if user.telegram_id == telegram_id:
                return user.id
        return None
    def get_user_id_tg(self, telegram_id: int) -> Optional[int]:
        """Возвращает Telegram ID пользователя по его Telegram ID, иначе None."""
        for user in self._user_id_tg:
            if user.telegram_id == telegram_id:
                return user.telegram_id
        return None
    