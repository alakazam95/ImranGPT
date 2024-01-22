from aiogram import types

import subscription
from config import bot, dp
from aiogram import Bot, Dispatcher, types
import data.creator as db
from data.creator import dbCreator as Database

db_creator = db.dbCreator()

modes = ['GPT-3.5', 'GPT-4', 'MIDJOURNEY-5.2', 'MIDJOURNEY-6']


#
# @dp.callback_query_handler(lambda c: c.data == 'help')
# async def process_callback_help(callback_query: types.CallbackQuery):
#     await bot.send_message(callback_query.from_user.id, "Здесь информация помощи...")
#

@dp.callback_query_handler(lambda c: c.data == 'subscribe')
async def process_callback_subscribe(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Информация о подписке...")


# обработчик для раздела /mode

# Предполагаем, что db_creator.get_subscription_type возвращает 'paid' или 'free'
@dp.callback_query_handler(lambda c: c.data in modes)
async def process_callback_mode_selection(callback_query: types.CallbackQuery):
    regime = ''
    subs_type = db_creator.get_subscription_type(callback_query.from_user.id)
    selected_mode = callback_query.data
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = []

    if selected_mode != 'gpt3.5' and subs_type != 'paid':
        subscription_message = "Доступ к этому режиму требует подписки. Используйте команду /pay для покупки подписки."
        await bot.send_message(callback_query.from_user.id, subscription_message)

    # Добавление кнопок с учетом текущего выбора пользователя
    for mode in modes:
        text = f"{'✅ ' if mode == selected_mode else ''}{mode}"
        callback_data = mode
        buttons.append(types.InlineKeyboardButton(text, callback_data=callback_data))

    # Добавление кнопок в клавиатуру
    keyboard.add(*buttons[:2])  # Добавляем первые две кнопки
    keyboard.add(*buttons[2:])  # Добавляем последние две кнопки

    # Отправляем или редактируем сообщение с клавиатурой
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=keyboard)
    print(selected_mode)



# @dp.callback_query_handler(lambda c: c.data in modes)
# async def process_callback_mode_selection(callback_query: types.CallbackQuery):
#     subs_n = db_creator.get_subscription_type(callback_query.from_user.id)
#     selected_mode = callback_query.data
#     keyboard = types.InlineKeyboardMarkup()
#     buttons = []
#
#     if selected_mode != 'gpt3.5' and not subs_n == 'paid':
#         subscription_message = "GPT-4 доступна в подписке по команде /pay" if selected_mode == 'gpt4' else "Генерация изображений с помощью MidJourney доступна в подписке по команде /pay"
#         await bot.send_message(callback_query.from_user.id, subscription_message)
#     for mode in modes:
#         text = f"{'✅ ' if mode == selected_mode and subs_n == 'paid' or mode == 'gpt3.5' else ''}{mode.upper()}"
#         callback_data = mode
#         buttons.append(types.InlineKeyboardButton(text, callback_data=callback_data))
#
#     # Добавляем кнопки по две в ряд
#     keyboard.row(buttons[0], buttons[1])
#     keyboard.row(buttons[2], buttons[3])


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


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def handle_successful_payment(message: types.Message):
    # Здесь обновите статус подписки пользователя в вашей базе данных
    db_creator.set_subscription_type(message.from_user.id, 'paid')
    subscription.activate_subscription(message.from_user.id)
    await message.reply("Спасибо за покупку подписки!")

