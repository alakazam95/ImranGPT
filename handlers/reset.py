from aiogram import types
from config import dp
import data.creator as db

db_manager = db.DBManager()


@dp.message_handler(commands=['reset'])
async def command_reset(message: types.Message):
    db_manager.clear_context_table(f'{message.from_user.username}_context')

    await message.reply("Контекст сброшен.")
