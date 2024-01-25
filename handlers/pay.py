from aiogram import types
from config import dp
import datetime
from datetime import datetime, timedelta

from aiogram import types

import data.creator as db
from config import bot, dp

db_creator = db.dbCreator()


@dp.message_handler(commands=['pay'])
async def command_pay(message: types.Message):
    if db_creator.get_subscription_type(message.from_user.id) == 'paid':
        await message.reply("у вас и так есть подписка")
        return

        # Логика для покупки подписки
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    paybutton = types.InlineKeyboardButton("pay", callback_data="pay")

    keyboard.add(paybutton)
    await message.reply("Опция покупки подписки: ...", reply_markup=keyboard)
