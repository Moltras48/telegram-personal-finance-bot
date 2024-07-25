import asyncio
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import kb 
import text

from .core import router
from states import MainState

from utils.add_expense import add_expenses
from utils.today_statistics import get_today_statistics
from utils.delete_expense import delete_expense
from utils.user_id_tg import Users_id_tg
from db.db import update_daily_limit, check_daily_limit

import re


@router.message()
async def add_expense(msg: Message, state: FSMContext):
    await state.set_state(MainState.in_main_menu)
    regexp_result = r'^\d+\s\w+$'
    regexp_delete = r'^/del\d+$'
    regexp_limit = r'^/limit'  # Регулярное выражение для обновления лимита
    regexp_limit_upd = r'^/ulimit\s\d+$'  # Регулярное выражение для обновления лимита
    if re.match(regexp_result, msg.text):  # Пример регулярного выражения для добавления расхода
        try:
            expense = add_expenses(msg.text, msg.from_user.id)
        except BaseException as e:
            await msg.answer(str(e))
            return
        answer_message = (
            f"Добавлены траты {expense.amount} руб на {expense.category_name}.\n\n"
            f"{get_today_statistics(msg.from_user.id)}")
        await asyncio.sleep(1)
        await msg.delete()
        await msg.answer(answer_message)
        await asyncio.sleep(2)
        await msg.answer(text.main_menu, reply_markup=kb.main_menu)
    elif re.match(regexp_delete, msg.text):  # Пример регулярного выражения для удаления расхода
        row_id = int(msg.text[4:])
        texts = delete_expense(row_id, msg.from_user.id)
        #answer_message = text.entry_delete
        answer_message = texts
        await asyncio.sleep(1)
        await msg.delete()
        await msg.answer(answer_message)
        await asyncio.sleep(2)
        await msg.answer(text.main_menu, reply_markup=kb.main_menu)
    elif re.match(regexp_limit, msg.text):  # Обработка команды для обновления лимита
        match = re.search(r'/limit', msg.text)
        if match:
            await msg.delete()
            id_user_tg = Users_id_tg().get_user_by_telegram_id(msg.from_user.id)
            limit_amount  = check_daily_limit(id_user_tg)
            await msg.answer(f'Ваш ежедневный лимит сейчас составляет: <code>{limit_amount[0][0]}</code> рублей.\n'
                            +'<i>Для обновления напишите /ulimit *число*. </i>')
            await msg.answer(text.main_menu, reply_markup=kb.main_menu)
        else:
            await msg.answer("Ошибка: неверный формат команды.")    
    elif re.match(regexp_limit_upd, msg.text):  # Обработка команды для обновления лимита
        match = re.search(r'/ulimit (\d+)', msg.text)
        if match:
            new_limit = int(match.group(1))
            id_user_tg = Users_id_tg().get_user_by_telegram_id(msg.from_user.id)
            update_daily_limit(new_limit, id_user_tg)
            await msg.delete()
            await msg.answer(text.daily_limit + f"{new_limit}")
            await msg.answer(text.main_menu, reply_markup=kb.main_menu)
        else:
            await msg.answer("Ошибка: неверный формат команды.")
    else:
        await msg.answer(
            ''
            "<b>Не могу понять сообщение!</b>\n"
            + "<i>Напишите сообщение в формате,</i>\n"
            + "<i>Например: </i><code>100 еда</code>\n"
            + "<i>Или /ulimit *число* </i> <code>Чтобы обновить лимит</code>")