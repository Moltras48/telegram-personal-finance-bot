import pytz
import datetime
import re
from db.db import insert
from typing import NamedTuple, Optional
from utils.categories_settings import Categories
from utils.user_id_tg import Users_id_tg
from utils.exceptions import NotCorrectMessage

class Message(NamedTuple):
    """Структура распаршенного сообщения о новом расходе"""
    amount: int
    category_text: str

class Expense(NamedTuple):
    """Структура добавленного в БД нового расхода"""
    id: Optional[int]
    amount: int
    category_name: str

def add_expenses(raw_message: str, user_id: int) -> Expense:
    """Добавляет новое сообщение.
    Принимает на вход текст сообщения, пришедшего в бот."""
    parsed_message = _parse_message(raw_message)
    
    category = Categories().get_category(parsed_message.category_text)
    
    # Получаем пользователя по его telegram_id
    user_id_tg = Users_id_tg().get_user_by_telegram_id(user_id)
    
    # Проверяем, найден ли пользователь
    if user_id_tg is None:
        raise ValueError(f"Пользователь с ID {user_id} не найден.")
    
    inserted_row_id = insert("expense", {
        "amount": parsed_message.amount,
        "created": _get_now_formatted(),
        "category_codename": category.codename,
        "raw_text": raw_message,
        "telegram_user_id" : user_id_tg
    })
    return Expense(id=None,
                   amount=parsed_message.amount,
                   category_name=category.name)
    
def _parse_message(raw_message: str) -> Message:
    """Парсит текст пришедшего сообщения о новом расходе."""
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise NotCorrectMessage(
            "Не могу понять сообщение. Напишите сообщение в формате, "
            "например:\n1500 метро")

    amount = regexp_result.group(1).replace(" ", "")
    category_text = regexp_result.group(2).strip().lower()
    return Message(amount=amount, category_text=category_text)

def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")

def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now
