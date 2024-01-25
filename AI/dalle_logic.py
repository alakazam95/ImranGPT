# import config
# from config import bot, dp, OPENAI_API_KEY
# import data.creator as db
# from aiogram import Bot, Dispatcher, types
# import openai
# from openai import OpenAI
#
#
# OPENAI_API_KEY = config.OPENAI_API_KEY
# db_creator = db.dbCreator()
# client = OpenAI(api_key=OPENAI_API_KEY)
#
# async def generate_image(prompt):
#     try:
#         response = await openai.images.generate(
#             model="dall-e-3",
#             prompt="a white siamese cat",
#             size="1024x1024",
#             quality="standard",
#             n=1,
#         )
#
#         return response.data[0]["url"]
#     except Exception as e:
#         print(f"Ошибка при генерации изображения: {e}")
#         return None