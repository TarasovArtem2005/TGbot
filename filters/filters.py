from aiogram.types import CallbackQuery


class PressedBookMark:
    def __call__(self, callback: CallbackQuery):
        return callback.data.startswith('bookmark')


class PressedDelBookMark:
    def __call__(self, callback: CallbackQuery):
        return callback.data.startswith('del_bookmark')


