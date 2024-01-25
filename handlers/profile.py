from aiogram import types
from config import dp
import data.creator as db


@dp.message_handler(commands=['profile'])
async def command_profile(message: types.Message):
    # Логика для отображения профиля пользователя
    db_creator = db.dbCreator()
    user_id = message.from_user.id
    if db_creator.get_subscription_type(user_id) == 'paid':
        await message.reply(
            f'''nickname {db_creator.get_nickname(user_id)}\nподписка {db_creator.get_subscription_type(user_id)}\nлимиты у вас платная подписка \nдата окончания подписки {db_creator.get_limit_update_date(user_id)}''')
        return
    await message.reply(
        f'''nickname {db_creator.get_nickname(user_id)}\nподписка {db_creator.get_subscription_type(user_id)}\nлимиты {db_creator.get_user_limit(user_id)}\nдата окончания подписки {db_creator.get_limit_update_date(user_id)}''')
