import openai
import config
from config import bot, dp, OPENAI_API_KEY
import data.creator as db
from aiogram import Bot, Dispatcher, types
from openai import OpenAI
import handlers.callback_handlers as ch
import tiktoken

OPENAI_API_KEY = config.OPENAI_API_KEY
db_creator = db.dbCreator()
client = OpenAI(api_key=OPENAI_API_KEY)


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def is_model_available(user_id, model):
    model_availability = {'gpt-3.5-turbo': db_creator.check_tokens_limit(user_id),
                          'gpt-4': db_creator.check_gpt4_limit(user_id),
                          'dalle': db_creator.check_dalle_limit(user_id),
                          # TODO изменить ключ (название midjourney) в соответствии с API
                          'midjourney-5.2': db_creator.get_midjourney52_limit(user_id),
                          'midjourney-6': db_creator.get_midjourney6_limit(user_id)
                          }
    return model_availability[model]


@dp.message_handler(lambda message: not message.text.startswith('/'))
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    db_creator.reset_tokens_limit(user_id)
    db_creator.renew_daily_limits(user_id)
    gptmodel = db_creator.get_user_mode(user_id)
    if not gptmodel:
        gptmodel = 'gpt-3.5-turbo'
        db_creator.set_user_mode(user_id, gptmodel)

    if is_model_available(user_id, gptmodel):
        tablename = f'{message.from_user.username}_context'
        global question
        question = message.text

        print(message.from_user.username)
        # Send user input to OpenAI GPT
        db_creator.create_context_table(tablename)

        # Сбор контекста для данного пользователя
        db_creator.add_context(user_id, question, "user", tablename)
        contant = db_creator.get_context(tablename)
        print(gptmodel)
        completion = client.chat.completions.create(
            model=gptmodel,
            messages=contant
        )
        answ = completion.choices[0].message
        print(answ.content)
        tokens = num_tokens_from_string(str(answ.content) + question, 'cl100k_base')
        db_creator.update_tokens_amount(user_id, tokens)
        await message.reply(answ.content)
        db_creator.add_context(0, answ.content, "assistant", tablename)
    else:
        await message.reply('у вас закончились токены')


def generate_image(prompt):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"{prompt}",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print(f"Ошибка при генерации изображения: {e}")
        return None
