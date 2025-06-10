from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



def all_jokes_kbd(joke_id: int) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Удалить", callback_data=f"delete_joke_{joke_id}"))
    keyboard.add(InlineKeyboardButton(text="Изменить", callback_data=f"update_joke_{joke_id}"))
    keyboard.adjust(2)
    return keyboard.as_markup()