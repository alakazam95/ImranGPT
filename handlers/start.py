from aiogram import types
from config import dp, bot

@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    help_button = types.InlineKeyboardButton(text="Help", callback_data="help")
    subscribe_button = types.InlineKeyboardButton(text="Купить подписку", callback_data="subscribe")

    keyboard.add(help_button, subscribe_button)

    await message.reply("Привет! Я ваш AI бот. Вот что я умею:", reply_markup=keyboard)
