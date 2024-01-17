from aiogram import types
from config import dp

@dp.message_handler(commands=['ask'])
async def command_ask(message: types.Message):
    # Логика для задания вопроса в группах
    await message.reply("Задайте ваш вопрос...")
