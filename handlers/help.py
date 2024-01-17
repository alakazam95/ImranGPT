from aiogram import types
from config import dp

@dp.message_handler(commands=['help'])
async def command_help(message: types.Message):
    await message.reply("Здесь информация помощи...")
