import config
from config import bot, dp, OPENAI_API_KEY
import data.creator as db
from aiogram import Bot, Dispatcher, types
from openai import OpenAI
import handlers.callback_handlers as ch
import data.limits_manage as lm
import tiktoken

OPENAI_API_KEY = config.OPENAI_API_KEY
db_manager = db.DBManager()
client = OpenAI(api_key=OPENAI_API_KEY)


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def is_model_available(user_id, model_limit):
    user = db_manager.get_user(user_id)
    if user['gpt_subscription_type'] is None and user['gpt3_tokens'] > 0:
        return 1

    if user[model_limit] > 0:
        return 1

    return 0


@dp.message_handler(lambda message: not message.text.startswith('/'))
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    user = db_manager.get_user(user_id)
    model_limit = ''
    gptmodel = user['cur_gpt_mode']
    print(gptmodel)

    if not gptmodel:
        gptmodel = 'gpt-3.5-turbo'
        db_manager.update_user(user_id, cur_gpt_mode='gpt-3.5-turbo')
        model_limit = 'gpt35_limit'

    if gptmodel == 'gpt-3.5-turbo':
        model_limit = 'gpt35_limit'
    if gptmodel == 'gpt-4':
        model_limit = 'gpt4_limit'

    if is_model_available(user_id, model_limit):
        # try:
        tablename = f'{message.from_user.username}_context'
        global question
        question = message.text

        print(message.from_user.username)
        db_manager.create_context_table(tablename)

        # Сбор контекста для данного пользователя
        db_manager.add_context(user_id, question, "user", tablename)
        contant = db_manager.get_context(tablename)
        print(gptmodel)
        completion = client.chat.completions.create(
            model=gptmodel,
            messages=contant
        )
        answ = completion.choices[0].message
        tokens = num_tokens_from_string(str(answ.content) + question, 'cl100k_base')
        lm.update_gpt_limits(user_id, gptmodel, tokens)
        await message.reply(answ.content)
        db_manager.add_context(0, answ.content, "assistant", tablename)

        # except Exception as e:
        #     await message.reply(e)
    else:
        await message.reply('у вас закончились токены')

# def generate_image(prompt):
#     try:
#         response = client.images.generate(
#             model="dall-e-3",
#             prompt=f"{prompt}",
#             size="1024x1024",
#             quality="standard",
#             n=1,
#         )
#         image_url = response.data[0].url
#         return image_url
#     except Exception as e:
#         print(f"Ошибка при генерации изображения: {e}")
#         return None
