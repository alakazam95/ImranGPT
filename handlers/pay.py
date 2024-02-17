from aiogram import types
import data.creator as db
from config import bot, dp
from data.subscription import valid_subscriptions


db_manager = db.DBManager()


@dp.message_handler(commands=['pay'])
async def command_pay(message: types.Message):
    # Проверяем, есть ли у пользователя активная подписка
    user_id = message.from_user.id
    user = db_manager.get_user(user_id)
    has_gpt_subscription = user['gpt_subscription_type'] in valid_subscriptions

    keyboard = types.InlineKeyboardMarkup(row_width=1)  # Для лучшей читаемости делаем одну кнопку на строку

    # Создаем кнопки для каждой подписки
    subscription_buttons = [
        types.InlineKeyboardButton("GPT Старт - 490 руб/мес", callback_data="pay_gpt_Старт"),
        types.InlineKeyboardButton("GPT Стандарт - 990 руб/мес", callback_data="pay_gpt_Стандарт"),
        types.InlineKeyboardButton("GPT Премиум - 2990 руб/мес", callback_data="pay_gpt_Премиум"),
        types.InlineKeyboardButton("Midjourney Старт - 290 руб/мес", callback_data="pay_mj_Старт"),
        types.InlineKeyboardButton("Midjourney Стандарт - 590 руб/мес", callback_data="pay_mj_Стандарт"),
        types.InlineKeyboardButton("Midjourney Премиум - 990 руб/мес", callback_data="pay_mj_Премиум")
    ]

    # Добавляем кнопки в клавиатуру
    keyboard.add(*subscription_buttons)
    description = """
Выберите тип подписки:\n
**GPT Старт** - **20** запросов GPT4 и **50** GPT3.5 в день\n
**GPT Стандарт** - **50** запросов GPT4 и **100** GPT3.5 в день\n
**GPT Премиум** -  безлимит\n
**Midjourney Старт** - **10** запросов в день\n
**Midjourney Стандарт** - **25** запросов в день\n
**Midjourney Премиум** - **50** запросов в день\n
    """
    await message.reply(description, reply_markup=keyboard)
