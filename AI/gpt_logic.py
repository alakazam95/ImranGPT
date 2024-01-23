from config import bot, dp
from aiogram import Bot, Dispatcher, types
from aiogram import Bot, Dispatcher, types
from openai import OpenAI

client = OpenAI()
# openai.api_key = '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'
OPENAI_API_KEY = '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'


@dp.message_handler()
async def handle_message(message: types.Message):
    # Send user input to OpenAI GPT
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"{message}"}
        ]
    )
    answ = completion.choices[0].message.content
    await message.reply(answ)


