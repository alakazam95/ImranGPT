from aiogram import Bot, Dispatcher
from subscribe_checker import BanMiddleware
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

script_dir = os.path.dirname(os.path.abspath(__file__))

DATABASE_PATH = os.path.join(script_dir, "data", "mydatabase.db")
OPENAI_API_KEY = ''

storage = MemoryStorage()

bot = Bot(token='')
dp = Dispatcher(bot, storage= storage)
dp.middleware.setup(BanMiddleware(bot))


MID_TOKEN = ""
