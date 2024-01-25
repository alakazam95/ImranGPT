import subscription
from config import bot, dp
from aiogram import types
import data.creator as db
import mode_manager as mm
import mode

db_creator = db.dbCreator()


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
@dp.callback_query_handler(lambda c: c.data in ['0', '1', '2', '3'])
async def process_callback_mode_selection(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    selected_mode_index = int(callback_query.data)
    modem = mm.ModeManager(user_id, selected_mode_index)

    # Проверка подписки и доступности режима
    if not mode.is_mode_available_for_user(modem.get_mode(), user_id):
        await mode.inform_user_about_subscription_requirements(callback_query)
        return

    # Сохраняем выбранный режим пользователя
    modem.set_mode()

    # Обновляем клавиатуру с учетом выбора пользователя
    keyboard = mode.build_mode_selection_keyboard(modem)
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text="Выберите режим:",
        reply_markup=keyboard
    )


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
