from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import data.creator as db
from config import bot, dp

db_manager = db.DBManager()


@dp.message_handler(commands=['profile'])
async def show_profile(message: types.Message):
    user_id = message.from_user.id
    user = db_manager.get_user(user_id)

    if not user:
        await message.answer("Профиль не найден.")
        return

    # Формирование сообщения
    profile_info = (
        f"ID: {user_id}\n"
        # f"Подписка: {subscription_info}\n"
        f"Лимиты по нейронкам: GPT-3.5 - {user['gpt35_limit']}, GPT-4 - {user['gpt4_limit']}, midjourney - {user['mj52_limit']}, \n"
        f"Кол-во токенов GPT-3.5 - {user['gpt3_tokens']}"
    )

    await message.answer(profile_info)
