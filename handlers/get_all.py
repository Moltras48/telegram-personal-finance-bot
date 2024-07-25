import os

import asyncio
from aiogram import F
from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext

import pandas as pd

import kb 
import text

from .core import router
from states import MainState

from utils.upload_data_db import upload_data_db


@router.callback_query(F.data == "get_all")
async def today_statistics(clbck: CallbackQuery, state: FSMContext):
    """Отправляет все траты в формате xlsx"""
    await state.set_state(MainState.in_main_menu)
    columns,rows = upload_data_db(clbck.from_user.id)
    # Сохраняем DataFrame в файл Excel
    df = pd.DataFrame(rows, columns=columns)
    # Переименовываем столбцы (если необходимо)
    new_columns = {
        "id": "ID расхода в бд",
        "amount": "Сумма расхода",
        "created": "Дата расхода",
        "category_codename": "Категория",
        "raw_text": "Запрос",
    }
    df.rename(columns=new_columns, inplace=True)
    
    # Удаляем столбец 'id', заменяя его на пустую строку или любое другое название
    df.drop('telegram_user_id', axis=1, inplace=True)
    
    filename = f"db/Выгрука данных о тратах.xlsx"
    df.to_excel(filename, index=False)
    # Отправляем файл пользователю
    doc = BufferedInputFile.from_file(filename, chunk_size=1024*1024*50)
    await clbck.message.answer_document(document=doc)
    await asyncio.sleep(2)
    os.remove(filename)
    await clbck.message.answer(text.main_menu, reply_markup=kb.main_menu)