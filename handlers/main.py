from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import kb 
import text

from .core import router
from states import MainState

from utils import check_password
from utils.user_id_tg import Users_id_tg
from db.db import add_users, add_user_daily_limit

@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    await state.set_state(MainState.password_not_entered)
    await msg.answer(text.start_text)
                   
@router.message(MainState.password_not_entered)
async def check_password_handler(msg: Message, state: FSMContext):
    if check_password(msg.text):
        await msg.answer(text.correct_password)
        """Добавляем юзера по его телеграм айди в базу users при правильном вводе пароля"""
        add_users(msg.from_user.id)
        id_user_tg = Users_id_tg().get_user_by_telegram_id(msg.from_user.id)
        add_user_daily_limit(id_user_tg)
        await state.set_state(MainState.in_main_menu) 
        await msg.answer(text.main_menu, reply_markup=kb.main_menu)         
    else:
        await msg.answer(text.incorrect_password)

@router.message(Command("menu"))
async def start_handler(msg: Message, state: FSMContext):
    await state.set_state(MainState.in_main_menu)
    await msg.answer(text.main_menu, reply_markup=kb.main_menu)
    
# @router.message(Command("limit"))
# async def start_handler(msg: Message, state: FSMContext):
#     await state.set_state(MainState.in_main_menu)
#     await msg.delete()
#     id_user_tg = Users_id_tg().get_user_by_telegram_id(msg.from_user.id)
#     limit_amount  = check_daily_limit(id_user_tg)
#     await msg.answer(f'Ваш ежедневный лимит сейчас составляет: <code>{limit_amount[0][0]}</code> рублей.\n'
#                      +'<i>Для обновления напишите /limit *число*. </i>')