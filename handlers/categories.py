import asyncio
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

import kb 
import text

from .core import router
from states import MainState

from utils.categories_settings import Categories

@router.callback_query(F.data == "categories")
async def categories_list(clbck: CallbackQuery, state: FSMContext):
    """Отправляет список категорий расходов"""
    await state.set_state(MainState.in_main_menu)
    categories = Categories().get_all_categories()
    await clbck.message.delete()
    answer_message = text.category_list +\
            ("\n* ".join([c.name+' ('+", ".join(c.aliases)+')' for c in categories]))
    await clbck.message.answer(answer_message)
    await asyncio.sleep(2)
    await clbck.message.answer(text.main_menu, reply_markup=kb.main_menu)  