import asyncio
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

import kb 
import text

from .core import router
from states import MainState

from utils.today_statistics import get_today_statistics


@router.callback_query(F.data == "today")
async def today_statistics(clbck: CallbackQuery, state: FSMContext):
    """Отправляет сегодняшнюю статистику трат"""
    await state.set_state(MainState.in_main_menu)
    answer_message = get_today_statistics(clbck.from_user.id)
    await clbck.message.delete()
    await clbck.message.answer(answer_message)
    await asyncio.sleep(2)
    await clbck.message.answer(text.main_menu, reply_markup=kb.main_menu)