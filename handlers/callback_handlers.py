import subscription
from config import bot, dp
from aiogram import types
import data.creator as db
from handlers.mode import create_mode_keyboard, mode_command_handler, valid_subscriptions
from datetime import datetime, timedelta

db_manager = db.DBManager()


@dp.callback_query_handler(lambda c: c.data == 'subscribe')
async def process_callback_subscribe(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Информация о подписке...")


# обработчик для раздела /mode

# Предполагаем, что db_manager.get_subscription_type возвращает 'paid' или 'free'

@dp.callback_query_handler(lambda c: c.data.startswith('gpt-'))
async def handle_mode_selection(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data  # 'gpt-3.5' или 'gpt-4'

    # Получение текущих настроек пользователя из базы данных и обновление
    db_manager.update_user(user_id, cur_gpt_mode=data)

    # Перезапрашиваем обновленные данные пользователя
    updated_user = db_manager.get_user(user_id)
    cur_gpt_mode = updated_user['cur_gpt_mode']
    has_gpt_subscription = updated_user['gpt_subscription_type'] in valid_subscriptions

    # Создаем и отправляем обновленную клавиатуру
    keyboard = create_mode_keyboard(cur_gpt_mode, has_gpt_subscription)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer("Режим обновлен!")


@dp.callback_query_handler(lambda c: c.data == 'pay')
async def process_callback_pay(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id

    # Здесь должна быть логика для определения стоимости подписки
    prices = [types.LabeledPrice(label="Подписка на месяц", amount=49900)]  # Стоимость в копейках

    await bot.send_invoice(
        chat_id,
        title="Подписка на сервисы ИИ",
        description="Месячная подписка на сервисы ИИ",
        provider_token="381764678:TEST:76035",
        currency="RUB",
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
    # Здесь обновите статус подписки пользователя в вашей базе данных
    db_manager.set_subscription_type(user_id, 'paid')

    new_daily_limit_update_date = (datetime.now() - timedelta(days=1))
    db_manager.set_daily_limit_update_date(user_id, new_daily_limit_update_date.strftime("%Y-%m-%d %H:%M:%S"))

    subscription.activate_subscription(message.from_user.id)
    await message.reply("Спасибо за покупку подписки!")
