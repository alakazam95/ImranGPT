from aiogram import types
from config import dp
import data.creator as db

db_creator = db.dbCreator()
modes = ['gpt-3.5-turbo', 'gpt-4', 'MIDJOURNEY-5.2', 'MIDJOURNEY-6']


@dp.message_handler(commands=['mode'])
async def command_mode(message: types.Message):
    user_id = message.from_user.id
    db_creator.set_user_mode(user_id, 'GPT-3.5')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(mode, callback_data=mode) for mode in modes]

    keyboard.row(*buttons[:2])
    keyboard.row(*buttons[2:])
    await message.reply("Выберите нейросеть:", reply_markup=keyboard)
