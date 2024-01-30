from aiogram import types
from config import dp, bot
import asyncio
from AI.gpt_logic import generate_image
import data.creator as db

db_creator = db.dbCreator()

# TODO добавить функцию снятия очков лимита на dalle


@dp.message_handler(commands=['img'])
async def command_img(message: types.Message):
    model = db_creator.get_user_mode()
    user_id = message.from_user.id
    text = message.get_args()  # Получите текст после команды /img
    print('aaaa')
    loop = asyncio.get_event_loop()

    image_url = await loop.run_in_executor(None, generate_image, text)
    if image_url:

        await message.reply_photo(photo=image_url)  # Отправляйте изображение пользователю
        print('лимит снял')
        db_creator.remove_limit(user_id, model)
    else:

        await message.reply("Не удалось сгенерировать изображение.")
