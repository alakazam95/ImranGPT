from aiogram import types
from config import dp
# from AI.gpt_logic import generate_image

@dp.message_handler(commands=['img'])
async def command_img(message: types.Message):
    # text = message.get_args()  # Получите текст после команды /img
    # image_url = await generate_image(text)  # Генерируйте изображение
    # if image_url:
    #     await message.reply_photo(photo=image_url)  # Отправляйте изображение пользователю
    # else:
    await message.reply("Не удалось сгенерировать изображение.")
