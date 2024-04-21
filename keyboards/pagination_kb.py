from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_markup(current_pagination: str):
    buttons = [InlineKeyboardButton(text='<<', callback_data='backward'),
               InlineKeyboardButton(text=current_pagination, callback_data='save_page'),
               InlineKeyboardButton(text='>>', callback_data='forward')]
    kb = InlineKeyboardBuilder()
    kb.row(*buttons)
    return kb.as_markup()


