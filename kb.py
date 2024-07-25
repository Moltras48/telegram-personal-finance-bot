from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_menu_buttons = [
    [InlineKeyboardButton(text="Сегодняшняя статистика", callback_data="today")],
    [InlineKeyboardButton(text="За текущий месяц", callback_data="month")],
    [InlineKeyboardButton(text="Последние внесённые расходы (до 10 записей)", callback_data="expenses")],
    [InlineKeyboardButton(text="Список категорий трат", callback_data="categories")],
    [InlineKeyboardButton(text="Выгрузить все траты в Excel", callback_data="get_all")],
]

main_menu = InlineKeyboardMarkup(inline_keyboard=main_menu_buttons)