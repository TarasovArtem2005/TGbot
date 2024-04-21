from aiogram.types import BotCommand
from aiogram import Bot
from lexicon.lexicon import LEXICON_COMMANDS


async def set_menu(bot: Bot):
    bot_commands = [BotCommand(command=text, description=description) for text, description in LEXICON_COMMANDS.items()]
    await bot.set_my_commands(commands=bot_commands)