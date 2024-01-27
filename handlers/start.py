from aiogram import types
from config import dp, bot
import data.creator as db
import subscription
from datetime import datetime, timedelta



@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    db_creator = db.dbCreator()
    user_id = message.from_user.id
    nickname = message.from_user.username  # Получение никнейма пользователя

    # Проверка, существует ли пользователь
    if db_creator.user_exists(user_id):
        # Если пользователь существует, обновляем его никнейм
        if db_creator.get_nickname(user_id) != nickname:
            db_creator.set_nickname(user_id, nickname)
            await bot.send_message(user_id, "Ваш никнейм обновлен.")
    elif not db_creator.user_exists(user_id):
        # Если пользователя нет, добавляем его в базу данных
        db_creator.add_user(user_id, nickname)  # Предполагается, что add_user умеет обрабатывать nickname

        old_date = datetime.now() - timedelta(days=30)
        db_creator.set_daily_limit_update_date(user_id, old_date.strftime('%Y-%m-%d %H:%M:%S'))
        db_creator.set_limit_update_date(user_id, old_date.strftime('%Y-%m-%d %H:%M:%S'))
        print('not exist')
        subscription.activate_subscription(user_id)
        await bot.send_message(user_id, "Вы зарегистрированы.")

    # В вашем обработчике сообщений
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
