from aiogram import types
from config import bot, dp
from aiogram import Bot, Dispatcher, types
import data.creator as db
import markups as nav
from data.creator import dbCreator as Database

modes = ['gpt3.5', 'gpt4', 'midjourney5.2', 'midjourney6']


@dp.callback_query_handler(lambda c: c.data == 'help')
async def process_callback_help(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Здесь информация помощи...")


@dp.callback_query_handler(lambda c: c.data == 'subscribe')
async def process_callback_subscribe(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Информация о подписке...")


# обработчик для раздела /mode
@dp.callback_query_handler(lambda c: c.data in modes)
async def process_callback_mode_selection(callback_query: types.CallbackQuery):
    podpiska = 0
    selected_mode = callback_query.data
    keyboard = types.InlineKeyboardMarkup()
    buttons = []

    if selected_mode != 'gpt3.5' and not podpiska:
        subscription_message = "GPT-4 доступна в подписке по команде /pay" if selected_mode == 'gpt4' else "Генерация изображений с помощью MidJourney доступна в подписке по команде /pay"
        await bot.send_message(callback_query.from_user.id, subscription_message)
    for mode in modes:
        text = f"{'✅ ' if mode == selected_mode and podpiska or mode == 'gpt3.5' else ''}{mode.upper()}"
        callback_data = mode
        buttons.append(types.InlineKeyboardButton(text, callback_data=callback_data))

    # Добавляем кнопки по две в ряд
    keyboard.row(buttons[0], buttons[1])
    keyboard.row(buttons[2], buttons[3])