from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from aiogram.filters.callback_data import CallbackData

class Buttons(CallbackData, prefix='bookmark'):
    a: int
    b: int

def create_bookmark(marks: set[str]):
    lst = []
    for mark in sorted(marks, key=lambda x: int(x.split('--')[0])):
        lst.append(InlineKeyboardButton(text=mark, callback_data=f'bookmark_{mark.split("--")[0]}'))
    kb = InlineKeyboardBuilder()
    kb.row(*lst, width=1)
    kb.row(InlineKeyboardButton(text=LEXICON['edit_bookmarks_button'], callback_data='edit_bookmarks_button'),
          InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel'))
    return kb.as_markup()


def cancel_bookmark(marks: set[str]):
    lst = [InlineKeyboardButton(text=f'{LEXICON["del"]}{mark}', callback_data=f'del_bookmark_{mark.split("--")[0]}') for mark in marks]
    kb = InlineKeyboardBuilder()
    kb.row(*lst, width=1)
    kb.row(InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel_del'))
    return kb.as_markup()