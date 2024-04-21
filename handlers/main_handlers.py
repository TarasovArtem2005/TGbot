from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from lexicon.lexicon import LEXICON
from database.database import user_dict_template, users_db
from servives.file_handling import book
from keyboards.pagination_kb import create_markup
from keyboards.bookmark_kb import create_bookmark, cancel_bookmark
from filters.filters import PressedBookMark, PressedDelBookMark
from copy import deepcopy

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text=LEXICON['/start'])


@router.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer(text=LEXICON['/help'])


@router.message(Command(commands=['beginning']))
async def beginning_command(message: Message):
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)
    await message.answer(text=book[1], reply_markup=create_markup(f'1/{len(book)}'))


@router.message(Command(commands=['continue']))
async def continue_command(message: Message):
    await message.answer(text=book[users_db[message.from_user.id]['page']], reply_markup=create_markup(f'{users_db[message.from_user.id]["page"]}/{len(book)}'))


@router.message(Command(commands=['bookmarks']))
async def bookmarks_command(message: Message):
    if users_db[message.from_user.id]['bookmarks']:
        await message.answer(text='Это список ваших закладок', reply_markup=create_bookmark(users_db[message.from_user.id]['bookmarks']))
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


@router.callback_query(F.data == 'forward')
async def forward_callback(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] + 1 <= len(book):
        users_db[callback.from_user.id]['page'] += 1
        page = users_db[callback.from_user.id]['page']
        await callback.message.edit_text(text=book[page], reply_markup=create_markup(f'{page}/{len(book)}'))
    await callback.answer()


@router.callback_query(F.data == 'backward')
async def backward_callback(callback: CallbackQuery):
    page = users_db[callback.from_user.id]['page']
    if page - 1 != 0:
        users_db[callback.from_user.id]['page'] -= 1
        await callback.message.edit_text(text=book[page - 1], reply_markup=create_markup(f'{page - 1}/ {len(book)}'))
    await callback.answer()


@router.callback_query(F.data == 'save_page')
async def save_page_callback(callback: CallbackQuery):
    page_num = users_db[callback.from_user.id]['page']
    users_db[callback.from_user.id]['bookmarks'].add(f'{page_num}--{book[page_num]}')
    await callback.answer()


@router.callback_query(PressedBookMark())
async def bookmark_callback(callback: CallbackQuery):
    page_num = int(callback.data.split('_')[1])
    await callback.message.answer(text=book[page_num])


@router.callback_query(F.data == 'cancel')
async def cancel_callback(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(F.data == 'edit_bookmarks_button')
async def edit_bookmark_callback(callback: CallbackQuery):
    marks = users_db[callback.from_user.id]['bookmarks']
    await callback.message.answer(text=LEXICON['edit_bookmarks'], reply_markup=cancel_bookmark(marks))


@router.callback_query(PressedDelBookMark())
async def del_bookmark_callback(callback: CallbackQuery):
    page_num = int(callback.data.split('_')[2])
    users_db[callback.from_user.id]['bookmarks'].remove(f'{page_num}--{book[page_num]}')
    marks = users_db[callback.from_user.id]['bookmarks']
    if len(marks) != 0:
        await callback.message.edit_text(text=LEXICON['edit_bookmarks'], reply_markup=cancel_bookmark(marks))
    else:
        await callback.message.edit_text(text=LEXICON['edit_bookmarks'], reply_markup=cancel_bookmark(marks))
        await callback.message.answer(text=LEXICON['no_bookmarks'])


@router.callback_query(F.data == 'cancel_del')
async def cancel_del_callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON['cancel_text'])

