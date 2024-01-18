from aiogram import types
from config import bot, dp
from aiogram import Bot, Dispatcher, types
import markups as nav
from data.creator import dbCreator as Database

modes = ['gpt3.5', 'gpt4', 'midjourney5.2', 'midjourney6']


@dp.callback_query_handler(lambda c: c.data == 'help')
async def process_callback_help(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Здесь информация помощи...")


@dp.callback_query_handler(lambda c: c.data == 'subscribe')
async def process_callback_subscribe(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Информация о подписке...")


# @dp.callback_query_handler(lambda c: c.data == 'myid')
# async def process_callback_subscribe(callback_query: types.CallbackQuery):
#     user_id = message.from_user.id
#     await bot.send_message(callback_query.from_user.id, f"your id is {user_id}")

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

#
# db = Database("C:\\Users\\job_j\\Documents\\GitHub\\amed\\ImranGPT\\data\\mydatabase.db")
#
#
# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     if not db.user_exists(message.from_user.id):
#         db.add_user(message.from_user.id)
#         await bot.send_message(message.from_user.id, "Укажите ваш ник")
#     else:
#         await bot.send_message(message.from_user.id, "Вы уже зарегистрированы", reply_markup=nav.mainMenu)
#
#
# @dp.message_handler()
# async def bot_message(message: types.Message):
#     if message.chat.type == 'private':
#         if message.text == "🫂 ПРОФИЛЬ":
#             pass  # Тут должен быть код для обработки профиля
#         else:
#             if db.get_signup(message.from_user.id) == "setnickname":
#                 if len(message.text) > 15:
#                     await bot.send_message(message.from_user.id, "не больше 15 символов")
#                 elif '@' in message.text or '/' in message.text:
#                     await bot.send_message(message.from_user.id, "вы ввели запрещенный символ")
#                 else:
#                     db.set_nickname(message.from_user.id, message.text)
#                     db.set_signup(message.from_user.id, "done")
#                     await bot.send_message(message.from_user.id, "вы зарегистрированы", reply_markup=nav.mainMenu)
#             else:
#                 await bot.send_message(message.from_user.id, "Что?")
