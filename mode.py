from aiogram import types
from config import dp
import data.creator as db
import mode_manager as mm
import config

db_creator = db.dbCreator()
indxs = ['0', '1', '2', '3']


async def inform_user_about_subscription_requirements(callback_query: types.CallbackQuery):
    subscription_message = "Доступ к этому режиму требует подписки."
    await config.bot.send_message(callback_query.from_user.id, subscription_message)


def is_mode_available_for_user(mode: str, user_id: int) -> bool:
    sub_type = db_creator.get_subscription_type(user_id)
    if sub_type == 'paid' and (mode == 'gpt-3.5-turbo' or mode == 'gpt-4'):
        return True
    return False


def build_mode_selection_keyboard(modem) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=2)  # Установите количество кнопок в ряду
    buttons = []

    # Создание списка кнопок
    for index, mode_name in enumerate(modem.get_modenames()):
        text = f"{'✅ ' if modem.get_index() == index else ''}{mode_name}"
        callback_data = str(index)
        buttons.append(types.InlineKeyboardButton(text, callback_data=callback_data))

    # Добавление кнопок в клавиатуру парами
    while buttons:
        row = buttons[:2]  # Получаем первые две кнопки из списка
        keyboard.add(*row)  # Добавляем эти кнопки в новый ряд клавиатуры
        buttons = buttons[2:]  # Обновляем список кнопок, удаляя добавленные

    return keyboard

#test
@dp.message_handler(commands=['mode'])
async def command_mode(message: types.Message):
    user_id = message.from_user.id
    modem = mm.ModeManager(user_id)
    indxs = modem.get_modeindexes()
    # db_creator.set_user_mode(user_id, 'gpt-3.5-turbo')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton((modem.get_modenames())[int(i)], callback_data=i) for i in indxs]
    keyboard.row(*buttons[:2])
    keyboard.row(*buttons[2:])
    await message.reply("Выберите нейросеть:", reply_markup=keyboard)
