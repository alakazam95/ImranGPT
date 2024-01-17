from aiogram import types
from config import dp

@dp.message_handler(commands=['profile'])
async def command_profile(message: types.Message):
    # Логика для отображения профиля пользователя
    await message.reply("Информация о вашем профиле: ...")
