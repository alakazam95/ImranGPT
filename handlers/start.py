from aiogram import types
from config import dp, bot
import data.creator as cr
import data.returner as rr


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    # keyboard = types.InlineKeyboardMarkup(row_width=2)
    # help_button = types.InlineKeyboardButton(text="Help", callback_data="help")
    # subscribe_button = types.InlineKeyboardButton(text="Купить подписку", callback_data="subscribe")
    #
    # keyboard.add(help_button, subscribe_button)
    # user_id = message.from_user.id

    # В вашем обработчике сообщений
    user_id = message.from_user.id
    db_creator = cr.dbCreator()
    db_creator.add_user(user_id, 'basic', 50000, '2024-05-12')

    print(db_creator.get_users())



    await message.reply('''
Это бот ChatGPT + MidJourney в Telegram. Чтобы задать вопрос, просто напишите его.  
*Команды*
/start - перезапуск
/mode - выбрать нейросеть
/profile - профиль пользователя
/pay - купить подписку
/reset - сброс контекста
/img - генерация изображений
/blend - смешивание изображений
/help - помощь
/ask - задать вопрос (в группах)''')
