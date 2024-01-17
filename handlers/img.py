from aiogram import types
from config import dp

@dp.message_handler(commands=['img'])
async def command_img(message: types.Message):
    # Логика для генерации изображений
    await message.reply("Генерация изображения...")
