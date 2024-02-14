from aiogram import types
from config import dp
import data.creator as db
from datetime import datetime, timedelta

db_manager = db.DBManager()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user = db_manager.get_user(user_id)

    # Если пользователь не найден в базе данных, создаем новую запись
    if not user:
        free_gpt_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db_manager.add_user(user_id=user_id, nickname=message.from_user.username,
                            gpt_subscription_type=None, mj_subscription_type=None,
                            cur_gpt_mode=None, cur_mj_mode=None, gpt3_free_tokens_update_date=free_gpt_date,
                            gpt3_tokens=50000, mj52_limit=0, mj6_limit=0, gpt4_limit=0, gpt35_limit=0)
        user = db_manager.get_user(user_id)  # Повторно получаем данные после создания

    intro_text = "Привет! Я ваш помощник-бот. Вот что я могу:"
    commands_list = (
        "/start - показать это сообщение\n"
        "/profile - показать ваш профиль\n"
        "/mode - выбрать режим работы\n"
        "/pay - купить подписку\n"
        "/reset - сброс контекста\n"
        "/img - генерация изображений\n"
        "/blend - смешивание изображений\n"
        "/help - помощь\n"
        "/ask - задать вопрос (в группах)\n"
    )
    await message.answer(f"{intro_text}\n\n{commands_list}")
