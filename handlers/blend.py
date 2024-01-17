from aiogram import types
from config import dp

@dp.message_handler(commands=['blend'])
async def command_blend(message: types.Message):
    # Логика для смешивания изображений
    await message.reply("Смешивание изображений...")
