from aiogram import types
from config import dp

@dp.message_handler(commands=['mode'])
async def command_mode(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button_gpt35 = types.InlineKeyboardButton("✅GPT-3.5", callback_data="gpt3.5")
    button_gpt4 = types.InlineKeyboardButton("GPT-4", callback_data="gpt4")
    button_mj52 = types.InlineKeyboardButton("MidJourney 5.2", callback_data="midjourney5.2")
    button_mj6 = types.InlineKeyboardButton("MidJourney 6", callback_data="midjourney6")

    keyboard.add(button_gpt35, button_gpt4, button_mj52, button_mj6)

    await message.reply("Выберите нейросеть:", reply_markup=keyboard)
