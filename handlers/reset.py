from aiogram import types
from config import dp

@dp.message_handler(commands=['reset'])
async def command_reset(message: types.Message):
    # Логика для сброса контекста
    await message.reply("Контекст сброшен.")
