from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import json
from io import BytesIO
import asyncio
import aiohttp
import config
from config import bot, dp
import data.limits_manage as lm
from aiogram.dispatcher.filters import Command, Text


class Form(StatesGroup):
    waiting_for_user_input = State()
    waiting_user_btn = State()
    block = State()
    blend = State()
    face_swap = State()


MID_TOKEN = config.MID_TOKEN


async def generate_image(prompt: str, user_id):
    user = lm.db_manager.get_user(user_id)  # Получаем информацию о пользователе
    if not (user['mj_subscription_type'] and user['mj52_limit'] > 0):
        # Возвращаем ошибку или сообщение о недостатке лимитов
        return False, "У вас нет активной подписки Midjourney или закончились лимиты."

    url = "https://api.mymidjourney.ai/api/v1/midjourney/imagine"
    payload = {"prompt": prompt}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MID_TOKEN}",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            await asyncio.sleep(15)
            if response.status == 200:
                response_data = await response.json()
                lm.update_gpt_limits(user_id, 'midjourney5.2', 1)
                print(response_data, 'лимит отнялся, миджорни')

                await asyncio.sleep(15)

                return await midle_check(response_data)
            else:
                print("Error:", response.status)
                return False, False


async def button_click(do, message_id):
    url = "https://api.mymidjourney.ai/api/v1/midjourney/button"
    payload = {
        "messageId": f"{message_id}",
        "button": f"{do}"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MID_TOKEN}",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json.dumps(payload), headers=headers) as response:
            await asyncio.sleep(15)
            if response.status == 200:
                response_data = await response.json()
                print(response_data)
                await asyncio.sleep(15)
                return await midle_check(response_data)
            else:
                print("Error:", response.status)
                return False, False


async def midle_check(response_data):
    url = f"https://api.mymidjourney.ai/api/v1/midjourney/message/{response_data['messageId']}"
    headers = {
        "Authorization": f"Bearer {MID_TOKEN}",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                response_json = await response.json()
                print(response_json)
                if 'error' in response_json:
                    return False, False

                if response_json.get('progress', 0) != 100:
                    await asyncio.sleep(15)
                    return await midle_check(response_json)
                else:
                    message_id = response_json['messageId']
                    async with session.get(response_json['uri']) as image_response:
                        if image_response.status == 200:
                            image_bytes = BytesIO(await image_response.read())
                            # Отправка изображения
                            return types.InputFile(image_bytes, filename="image.png"), message_id

            elif response.status == 429:
                print("Error", response.status)
                await asyncio.sleep(30)
                return await midle_check(response_data)

            else:
                print("Error:", response.status)
                return False, False


async def blend(images, user_id):
    api_url = "https://api.mymidjourney.ai/api/v1/midjourney/blend"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MID_TOKEN}",
    }
    data = {"urls": images}
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, headers=headers, data=json.dumps(data)) as response:
            if response.status == 200:
                response_data = await response.json()
                lm.update_gpt_limits(user_id, 'midjourney5.2', 1)

                print(response_data, 'лимит отнялся, миджорни')
                await asyncio.sleep(30)
                return await midle_check(response_data)
            else:
                return f"Произошла ошибка: {response.status}"


async def face_swap(source, target):
    api_url = "https://api.mymidjourney.ai/api/v1/midjourney/faceswap"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MID_TOKEN}",
    }
    data = {"source": source, "target": target}
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, headers=headers, data=json.dumps(data)) as response:
            if response.status == 200:
                response_data = await response.json()
                print(response_data)
                await asyncio.sleep(50)
                return await midle_check(response_data)
            else:
                print(f"Произошла ошибка: {response.status}")
                return False, False


@dp.message_handler(state=Form.block)
@dp.callback_query_handler(state=Form.block)
async def block(input, state: FSMContext):
    await input.answer("Дождитесь обработки предыдущего запроса")


@dp.message_handler(commands=['imagine'], state='*')
async def process_start_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = lm.db_manager.get_user(user_id)  # Предполагаем, что функция get_user возвращает информацию о пользователе
    if user['mj_subscription_type'] and user['mj52_limit'] > 0:
        await state.set_state(Form.waiting_for_user_input)
        await message.reply("Введи промт")
    else:
        await message.reply("У вас нет активной подписки Midjourney или закончились лимиты.")


@dp.message_handler(commands=['face_swap'], state='*')
async def face_swap_main(message: types.Message, state: FSMContext):
    await state.finish()
    await state.set_state(Form.face_swap)
    await message.reply("Отправьте мне 2 ссылок на изображения, разделённых запятыми.")


@dp.message_handler(commands=['blend'], state='*')
async def start_blend(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = lm.db_manager.get_user(user_id)
    if user['mj_subscription_type'] and user['mj52_limit'] > 0:

        # user_id = message.from_user.id
        # processing_tasks.pop(user_id, None) #для блока с фото
        # photos_cash.pop(user_id, None)
        await state.finish()
        await state.set_state(Form.blend)
        await message.reply("Отправьте до 5 ссылок на изображения, разделённых запятыми.")
    else:
        await message.reply("У вас нет активной подписки Midjourney или закончились лимиты.")
        return


@dp.message_handler(state=Form.waiting_for_user_input)
async def user_input(message: types.Message, state: FSMContext, image_url=None, message_id=None, time_message=None):
    if message.text.startswith('/'):
        await state.finish()
        return

    user_id = message.from_user.id
    user_text = message.text
    await state.set_state(Form.block)
    if image_url is None:
        time_message = await message.answer("Идёт генерация...")
        image_url, message_id = await generate_image(user_text, user_id)
        await time_message.delete()

    else:
        await time_message.delete()

    if image_url:
        print(image_url, message_id)
        inline_kb_full = InlineKeyboardMarkup()
        inline_kb_full.row(InlineKeyboardButton('U1', callback_data='U1'),
                           InlineKeyboardButton('U2', callback_data='U2'),
                           InlineKeyboardButton('U3', callback_data='U3'),
                           InlineKeyboardButton('U4', callback_data='U4'), InlineKeyboardButton('🔄', callback_data='🔄'))
        inline_kb_full.row(InlineKeyboardButton('V1', callback_data='V1'),
                           InlineKeyboardButton('V2', callback_data='V2'),
                           InlineKeyboardButton('V3', callback_data='V3'),
                           InlineKeyboardButton('V4', callback_data='V4'))

        await state.update_data(message_id=message_id)
        await bot.send_photo(message.from_user.id, image_url, reply_markup=inline_kb_full)
        await state.set_state(Form.waiting_user_btn)

    else:
        await message.reply("Извините, не удалось сгенерировать изображение.")
        await state.finish()


@dp.callback_query_handler(state=Form.waiting_user_btn)
async def process_callback(callback, state: FSMContext):
    info = await state.get_data()
    message_id = info['message_id']
    await state.set_state(Form.block)

    user_id = callback.from_user.id
    callback_data = callback.data
    user = lm.db_manager.get_user(user_id)

    time_message = await callback.message.answer("Идёт генерация...")
    image, message_id = await button_click(callback.data, message_id)

    if image:
        if user['mj_subscription_type'] is None and not user['mj52_limit'] > 0:
            await callback.message.answer("У вас нет активной подписки Midjourney или закончились лимиты.")
            return

        inline_kb_full = InlineKeyboardMarkup()
        if callback.data in ['V1', 'V2', 'V3', 'V4', "🔄", 'Zoom Out 2x', 'Zoom Out 1.5x', 'Vary (Strong)',
                             'Vary (Subtle)']:

            '''отнимаю лимит'''
            lm.update_gpt_limits(user_id, 'midjourney5.2', 1)  # Обновляем лимиты для пользователя
            print('лимит отнялся, миджорни')

            inline_kb_full.row(InlineKeyboardButton('U1', callback_data='U1'),
                               InlineKeyboardButton('U2', callback_data='U2'),
                               InlineKeyboardButton('U3', callback_data='U3'),
                               InlineKeyboardButton('U4', callback_data='U4'),
                               InlineKeyboardButton('🔄', callback_data='🔄'))
            inline_kb_full.row(InlineKeyboardButton('V1', callback_data='V1'),
                               InlineKeyboardButton('V2', callback_data='V2'),
                               InlineKeyboardButton('V3', callback_data='V3'),
                               InlineKeyboardButton('V4', callback_data='V4'))
        else:
            if callback.data in ['Upscale (4x)', 'Upscale (2x)', 'Redo Upscale (2x)', 'Redo Upscale (4x)']:
                inline_kb_full.row(InlineKeyboardButton('Redo Upscale (2x)', callback_data="Redo Upscale (2x)"),
                                   InlineKeyboardButton("Redo Upscale (4x)", callback_data="Redo Upscale (4x)"))
                '''отнимаю лимит'''
                lm.update_gpt_limits(user_id, 'midjourney5.2', 1)  # Обновляем лимиты для пользователя
                print('лимит отнялся, миджорни')

            elif callback.data in ['⬅️', '➡️', '⬆️', '⬇️']:
                '''отнимаю лимит'''
                lm.update_gpt_limits(user_id, 'midjourney5.2', 1)  # Обновляем лимиты для пользователя
                print('лимит отнялся, миджорни')

                inline_kb_full.row(InlineKeyboardButton('U1', callback_data='U1'),
                                   InlineKeyboardButton('U2', callback_data='U2'),
                                   InlineKeyboardButton('U3', callback_data='U3'),
                                   InlineKeyboardButton('U4', callback_data='U4'),
                                   InlineKeyboardButton('🔄', callback_data='🔄'))

            else:
                '''отнимаю лимит'''
                lm.update_gpt_limits(user_id, 'midjourney5.2', 1)  # Обновляем лимиты для пользователя
                print('лимит отнялся, миджорни')

                inline_kb_full.row(InlineKeyboardButton('Upscale (2x)', callback_data="Upscale (2x)"),
                                   InlineKeyboardButton("Upscale (4x)", callback_data="Upscale (4x)"),
                                   InlineKeyboardButton("Zoom Out 2x", callback_data="Zoom Out 2x"),
                                   InlineKeyboardButton("Zoom Out 1.5x", callback_data="Zoom Out 1.5x"))
                inline_kb_full.row(InlineKeyboardButton("Vary (Strong)", callback_data="Vary (Strong)"),
                                   InlineKeyboardButton("Vary (Subtle)", callback_data="Vary (Subtle)"))
                inline_kb_full.row(InlineKeyboardButton("⬅️", callback_data="⬅️"),
                                   InlineKeyboardButton("➡️", callback_data="➡️"),
                                   InlineKeyboardButton("⬆️", callback_data="⬆️"),
                                   InlineKeyboardButton("⬇️", callback_data="⬇️"))

        await time_message.delete()

        await state.update_data(message_id=message_id)

        await state.set_state(Form.waiting_user_btn)

        await callback.message.answer_photo(image, reply_markup=inline_kb_full)
    else:
        await callback.message.answer("Извините, не удалось сгенерировать изображение.")
        await state.set_state(Form.waiting_user_btn)


"""ЭТО БЛОК ДЛЯ ФОТО АЛЬБОМОМ"""


# processing_tasks = {}  # Словарь для отслеживания задач обработки по пользователю
# photos_cash = {}
# @dp.message_handler(content_types=['photo'], state=Form.blend)
# async def handle_photos(message: types.Message, state: FSMContext):
#     user_id = message.from_user.id
#     async with state.proxy() as data:
#         if user_id not in photos_cash:
#             photos_cash[user_id] = []

#         file_info = await bot.get_file(message.photo[-1].file_id)
#         file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}"
#         if len(photos_cash[user_id]) < 5:
#             photos_cash[user_id].append(file_url)


#         if user_id in processing_tasks:
#             return

#         task = asyncio.create_task(start_processing_with_delay(user_id, message, state))
#         processing_tasks[user_id] = task


# async def start_processing_with_delay(user_id,  message, state):
#     await asyncio.sleep(5)  # Подождем немного на случай последующих фотографий
#     async with state.proxy() as data:
#         if user_id in processing_tasks:
#             await process_images(message, state, photos_cash[user_id])

@dp.message_handler(content_types=['text'], state=Form.blend)
async def blend_get_links(message: types.Message, state: FSMContext):
    if message.text.startswith('/'):
        await message.reply("Это команда. Пожалуйста, отправьте ссылки на изображения.")
        await state.finish()

        return
    links = message.text.replace(' ', '').replace('\n', '').split(',')
    if len(links) > 5:
        await message.reply("Пожалуйста, отправьте не более 5 ссылок.")
    else:

        await process_images(message, state, links)


async def process_images(message, state, images):
    await state.set_state(Form.block)
    time_message = await message.answer("Идёт генерация...")
    response, messageId = await blend(images, message.from_user.id)
    await user_input(message, state, response, messageId, time_message)


@dp.message_handler(content_types=['text'], state=Form.face_swap)
async def face_swap_get_links(message: types.Message, state: FSMContext):
    links = message.text.replace(' ', '').replace('\n', '').split(',')
    if len(links) > 2:
        await message.reply("Пожалуйста, отправьте не более 2 ссылок.")
    else:
        time_message = await message.answer("Идёт генерация...")

        response, messageId = await face_swap(links[0], links[1])
        await user_input(message, state, response, messageId, time_message)


@dp.message_handler(Text(startswith="/"), state="*")
async def handle_any_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        # Сброс состояния пользователя
        await state.finish()
        # Сообщение пользователю, что его предыдущее действие было отменено
        await message.reply("Текущая операция была отменена. Выберите команду для продолжения.")
