from aiogram import types
from config import dp



@dp.message_handler(commands=['myid'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    await message.reply(f"Ваш уникальный Telegram ID: {user_id}")
