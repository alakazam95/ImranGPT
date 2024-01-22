from aiogram import types
from config import dp

modes = ['GPT-3.5', 'GPT-4', 'MIDJOURNEY-5.2', 'MIDJOURNEY-6']


@dp.message_handler(commands=['mode'])
async def command_mode(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(mode, callback_data=mode) for mode in modes]

    keyboard.row(*buttons[:2])
    keyboard.row(*buttons[2:])
    await message.reply("Выберите нейросеть:", reply_markup=keyboard)
