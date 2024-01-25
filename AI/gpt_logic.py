import openai
import config
from config import bot, dp, OPENAI_API_KEY
import data.creator as db
from aiogram import Bot, Dispatcher, types
from openai import OpenAI
import tiktoken

OPENAI_API_KEY = config.OPENAI_API_KEY
db_creator = db.dbCreator()
client = OpenAI(api_key=OPENAI_API_KEY)


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


@dp.message_handler()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    db_creator.update_tokens_limit(user_id)
    if db_creator.check_tokens_limit(user_id):
        tablename = f'{message.from_user.username}_context'
        global question
        question = message.text
        gptmodel = db_creator.get_user_mode(user_id)
        print(message.from_user.username)
        # Send user input to OpenAI GPT
        db_creator.create_context_table(tablename)

        # amed.append({"role": "system", "content": question})
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

async def generate_image(prompt):
    try:
        response = await openai.images.generate(
            model="dall-e-3",
            prompt=f"{prompt}",
            size="1024x1024",
            quality="standard",
            n=1,
        )

        return response.data[0]["url"]
    except Exception as e:
        print(f"Ошибка при генерации изображения: {e}")
        return None