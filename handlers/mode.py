from aiogram import types, Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot, dp
import data.creator as db

db_manager = db.DBManager()


def create_mode_keyboard(cur_gpt_mode, cur_mj_mode, has_gpt_subscription, has_mj_subscription):
    gpt_mark = "✅"
    keyboard = InlineKeyboardMarkup(row_width=2)

    # Добавляем кнопки для GPT, если есть подписка
    if has_gpt_subscription:
        gpt_buttons = [
            InlineKeyboardButton(text=f"GPT-3.5{gpt_mark if cur_gpt_mode == 'gpt-3.5' else ''}", callback_data="gpt-3.5"),
            InlineKeyboardButton(text=f"GPT-4{gpt_mark if cur_gpt_mode == 'gpt-4' else ''}", callback_data="gpt-4"),
        ]
        keyboard.add(*gpt_buttons)

    # Добавляем кнопки для Midjourney, если есть подписка
    if has_mj_subscription:
        mj_buttons = [
            InlineKeyboardButton(text=f"MidJourney-5.2{gpt_mark if cur_mj_mode == 'midjourney-5.2' else ''}", callback_data="midjourney-5.2"),
            InlineKeyboardButton(text=f"MidJourney-6{gpt_mark if cur_mj_mode == 'midjourney-6' else ''}", callback_data="midjourney-6"),
        ]
        keyboard.add(*mj_buttons)

    return keyboard


@dp.message_handler(commands=['mode'])
async def mode_command_handler(message: types.Message):

    user_id = message.from_user.id
    user = db_manager.get_user(user_id)

    # Если пользователь не найден в базе данных, создаем новую запись
    if not user:
        db_manager.add_user(user_id=user_id, nickname=message.from_user.username,
                            gpt_subscription_type=None, mj_subscription_type=None,
                            gpt_sub_update_date=None, mj_sub_update_date=None,
                            cur_gpt_mode=None, cur_mj_mode=None,
                            gpt3_tokens=0, mj_daily_update_date=None, gpt_daily_update_date=None,
                            mj52_limit=0, mj6_limit=0, gpt4_limit=0, gpt35_limit=0)
        user = db_manager.get_user(user_id)  # Повторно получаем данные после создания

    cur_gpt_mode = user['cur_gpt_mode'] if user['cur_gpt_mode'] else "Не выбрано"
    cur_mj_mode = user['cur_mj_mode'] if user['cur_mj_mode'] else "Не выбрано"
    has_gpt_subscription = user['gpt_subscription_type'] is not None
    has_mj_subscription = user['mj_subscription_type'] is not None
    if has_gpt_subscription or has_mj_subscription:
        keyboard = create_mode_keyboard(cur_gpt_mode, cur_mj_mode, has_gpt_subscription, has_mj_subscription)
        await message.reply("Выберите режим:", reply_markup=keyboard)
    else:
        await message.reply("У вас нет активной подписки. Пожалуйста, подпишитесь для доступа к этим функциям.")
    #
    # await message.reply("Выберите режим:", reply_markup=keyboard)
