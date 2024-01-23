from config import bot, dp
import data.creator as db
from aiogram import Bot, Dispatcher, types
from openai import OpenAI

db_creator = db.dbCreator()
client = OpenAI()
# openai.api_key = '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'
OPENAI_API_KEY = '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'

amed = [{"role": "system", "content": ""}]


@dp.message_handler()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    tablename = f'{message.from_user.username}_context'
    global question
    question = message.text
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
