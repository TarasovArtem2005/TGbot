from aiogram import Bot, Dispatcher
from config_data.config import load_config
import handlers.other_handlers
import handlers.main_handlers
from keyboards.main_menu import set_menu
import asyncio
import logging


async def main():
    config = load_config()
    bot = Bot(token=config.tg_bot.tocken)
    await set_menu(bot)
    dp = Dispatcher()
    dp.include_router(handlers.main_handlers.router)
    dp.include_router(handlers.other_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())