from aiogram import types
from config import dp


@dp.message_handler(commands=['myid'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    await message.reply(f"Ваш уникальный Telegram ID: {user_id}")


@dp.message_handler(commands=['amed'])
async def sfulp(message: types.Message):
    user_id = message.from_user.id
    keyboard = types.InlineKeyboardMarkup(row_width=1)  # Для лучшей читаемости делаем одну кнопку на строку
    btn = types.InlineKeyboardButton("я заплатил 06", callback_data='sucpay')
    keyboard.add(btn)

    await message.reply(f"типо оплата_095", reply_markup=keyboard)
