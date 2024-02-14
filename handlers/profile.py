from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import data.creator as db
from config import bot, dp
from datetime import datetime, timedelta


db_manager = db.DBManager()


@dp.message_handler(commands=['profile'])
async def show_profile(message: types.Message):
    user_id = message.from_user.id
    user = db_manager.get_user(user_id)
    subscriptions = user['mj_subscription_type'], user['gpt_subscription_type']

    gpt_sub_update_date = datetime.strptime(user['gpt_sub_update_date'], "%Y-%m-%d %H:%M:%S")
    gpt_sub_end_date = gpt_sub_update_date + timedelta(days=30)  # Длительность подписки 30 дней

    mj_sub_update_date = datetime.strptime(user['mj_sub_update_date'], "%Y-%m-%d %H:%M:%S")
    mj_sub_end_date = mj_sub_update_date + timedelta(days=30)  # Длительность подписки 30 дней

    if not user:
        await message.answer("Профиль не найден.")
        return

    # Формирование сообщения
    profile_info = (
        f"ID: {user['nickname']}\n"
        f"Подписки: midjourney - {subscriptions[0]}, GPT - {subscriptions[1]}\n\n"
        f"Лимиты по нейронкам:\nGPT-3.5 - {user['gpt35_limit']}\nGPT-4 - {user['gpt4_limit']}\nmidjourney - {user['mj52_limit']}, \n\n"
        f"Кол-во токенов GPT-3.5 - {user['gpt3_tokens']}\n"
        f"Дата окончания подписки\nmidjourney - {mj_sub_end_date}\nGPT - {gpt_sub_end_date}\n"

    )

    await message.answer(profile_info)
