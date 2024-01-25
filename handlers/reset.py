from aiogram import types
from config import dp
import data.creator as db

db_creator = db.dbCreator()


@dp.message_handler(commands=['reset'])
async def command_reset(message: types.Message):
    db_creator.delete_user_questions(f'{message.from_user.username}_context')

    await message.reply("Контекст сброшен.")
