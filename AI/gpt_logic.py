import config
from config import bot, dp, OPENAI_API_KEY
import data.creator as db
from aiogram import Bot, Dispatcher, types
import openai
from openai import OpenAI


OPENAI_API_KEY = config.OPENAI_API_KEY
db_creator = db.dbCreator()
client = OpenAI(api_key=OPENAI_API_KEY)


@dp.message_handler()
async def handle_message(message: types.Message):

    user_id = message.from_user.id
    tablename = f'{message.from_user.username}_context'
    global question
    question = message.text
    model = db_creator.get_user_mode(user_id)
    print(message.from_user.username)
    # Send user input to OpenAI GPT
    db_creator.create_context_table(tablename)

    # amed.append({"role": "system", "content": question})
    # Сбор контекста для данного пользователя
    db_creator.add_context(user_id, question, "user", tablename)
    contant = db_creator.get_context(tablename)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=contant
    )
    answ = completion.choices[0].message
    await message.reply(answ.content)
    db_creator.add_context(0, answ.content, "assistant", tablename)
