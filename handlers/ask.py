from aiogram import types
from config import dp

@dp.message_handler(commands=['ask'], chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP])
async def ask_command_in_group(message: types.Message):
    pass
    # Логика обработки команды в групповом чате

@dp.message_handler(commands=['ask'])
async def ask_command_elsewhere(message: types.Message):
    # Сообщение, отправляемое, если команда вызвана вне группового чата
    await message.reply("Эта команда доступна только в групповых чатах.")
