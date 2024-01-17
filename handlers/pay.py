from aiogram import types
from config import dp

@dp.message_handler(commands=['pay'])
async def command_pay(message: types.Message):
    # Логика для покупки подписки
    await message.reply("Опция покупки подписки: ...")
