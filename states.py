from aiogram.fsm.state import StatesGroup, State


class MainState(StatesGroup):
    password_not_entered = State()
    in_main_menu = State()
