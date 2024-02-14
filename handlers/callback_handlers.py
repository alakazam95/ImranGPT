import subscription
from config import bot, dp
from aiogram import types
import data.creator as db
from handlers.mode import create_mode_keyboard, mode_command_handler
from data.subscription import valid_subscriptions, GPTSubscription, MJSubscription
from datetime import datetime, timedelta

db_manager = db.DBManager()


@dp.callback_query_handler(lambda c: c.data == 'subscribe')
async def process_callback_subscribe(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Информация о подписке...")


@dp.callback_query_handler(lambda c: c.data.startswith('gpt-'))
async def handle_mode_selection(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data  # 'gpt-3.5' или 'gpt-4'

    # Получение текущих настроек пользователя из базы данных и обновление
    db_manager.update_user(user_id, cur_gpt_mode=data)

    # Перезапрашиваем обновленные данные пользователя
    updated_user = db_manager.get_user(user_id)
    cur_gpt_mode = updated_user['cur_gpt_mode']
    gpt_subscription = updated_user['gpt_subscription_type']

    # Создаем и отправляем обновленную клавиатуру
    keyboard = create_mode_keyboard(cur_gpt_mode, gpt_subscription)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer("Режим обновлен!")


@dp.callback_query_handler(lambda c: c.data.startswith('pay'))
async def process_callback_pay(callback_query: types.CallbackQuery):
    await callback_query.answer()  # Отвечаем на callback, чтобы убрать часики в Telegram

    user_id = callback_query.from_user.id
    subscription_choice = callback_query.data

    user = db_manager.get_user(user_id)
    _, aitype, temp_sub = subscription_choice.split('_')
    if user[f'{aitype}_subscription_type'] == temp_sub:
        await callback_query.answer('sdfdfdf')
        return

    db_manager.update_user(user['user_id'], temp_subscription=subscription_choice)

    # Словарь с ценами подписок (в копейках)
    subscription_prices = {
        "pay_gpt_Старт": 49000,
        "pay_gpt_Стандарт": 99000,
        "pay_gpt_Премиум": 299000,
        "pay_mj_Старт": 29000,
        "pay_mj_Стандарт": 59000,
        "pay_mj_Премиум": 99000
    }

    price = subscription_prices[subscription_choice]
    title = "Подписка на сервисы ИИ"
    description = "Месячная подписка на сервисы ИИ"
    currency = "RUB"
    prices = [types.LabeledPrice(label="Подписка", amount=price)]
    # prices = [types.LabeledPrice(label="Подписка на месяц", amount=49900)]  # Стоимость в копейках

    await bot.send_invoice(
        user_id,
        title=title,
        description=description,
        provider_token="381764678:TEST:76035",
        currency=currency,
        prices=prices,
        payload="UNIQUE_PAYLOAD",
        start_parameter="start",
    )



@dp.pre_checkout_query_handler()
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.callback_query_handler(lambda c: c.data == 'keyerr')
async def key_error(message: types.Message):
    await message.reply("вы не выбрали нейросеть! /mode")


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def handle_successful_payment(message: types.Message):
    user_id = message.from_user.id
    user = db_manager.get_user(user_id)
    sub_choice = user['temp_subscription']
    print(sub_choice)

    _, aitype, temp_sub = sub_choice.split('_')

    print(temp_sub)
    subscription_class = 0
    db_manager.update_user(user['user_id'], temp_subscription=0)

    # Определяем параметры подписки на основе полученного типа
    if aitype == 'gpt':
        subscription_class = GPTSubscription(db_manager, temp_sub)
    elif aitype == 'mj':
        subscription_class = MJSubscription(db_manager, temp_sub)

    if subscription_class:
        subscription_class.activate(user_id)
        await message.reply("Спасибо за покупку подписки! Ваша подписка активирована.")
    else:
        await message.reply("Произошла ошибка при активации подписки.")
