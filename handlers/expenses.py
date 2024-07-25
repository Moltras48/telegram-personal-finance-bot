import asyncio
from aiogram import F, exceptions
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

import kb 
import text

from .core import router
from states import MainState

from utils.last_expenses import last


@router.callback_query(F.data == "expenses")
async def today_statistics(clbck: CallbackQuery, state: FSMContext):
    """Отправляет последние несколько записей о расходах"""
    await state.set_state(MainState.in_main_menu)
    last_expenses = last(clbck.from_user.id)
    try:
        await clbck.message.delete()
    except exceptions.TelegramBadRequest:
        pass
    if not last_expenses:
        await clbck.message.answer(text.no_expenses)
        await asyncio.sleep(2)
        await clbck.message.answer(text.main_menu, reply_markup=kb.main_menu)
        return

    last_expenses_rows = [
        f"{expense.amount} руб. на {expense.category_name} — нажми "
        f"/del{expense.id} для удаления"
        for expense in last_expenses]
    answer_message = text.resent_expenses + "\n\n* "\
            .join(last_expenses_rows)
    try:
        await clbck.message.delete()
    except exceptions.TelegramBadRequest:
        pass
    await clbck.message.answer(answer_message)
    await asyncio.sleep(2)
    await clbck.message.answer(text.main_menu, reply_markup=kb.main_menu)