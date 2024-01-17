from aiogram import types
from config import bot, dp

@dp.callback_query_handler(lambda c

: c.data == 'help')
async def process_callback_help(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Здесь информация помощи...")

@dp.callback_query_handler(lambda c: c.data == 'subscribe')
async def process_callback_subscribe(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Информация о подписке...")