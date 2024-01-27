from aiogram import types
from config import dp, bot
import asyncio
from AI.gpt_logic import generate_image


@dp.message_handler(commands=['img'])
async def command_img(message: types.Message):
    text = message.get_args()  # Получите текст после команды /img
    print('aaaa')
    loop = asyncio.get_event_loop()

    image_url = await loop.run_in_executor(None, generate_image, text)
    if image_url:
        await message.reply_photo(photo=image_url)  # Отправляйте изображение пользователю
    else:
        await message.reply("Не удалось сгенерировать изображение.")
