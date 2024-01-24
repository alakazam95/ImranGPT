from aiogram import Bot, Dispatcher
from subscribe_checker import BanMiddleware
import os


script_dir = os.path.dirname(os.path.abspath(__file__))

DATABASE_PATH = os.path.join(script_dir, "data", "mydatabase.db")
OPENAI_API_KEY = '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'
bot = Bot(token='6727239369:AAFxy9hXV14G3bjXrj6CXC2Rt4LMFUbyiXA')
dp = Dispatcher(bot)
dp.middleware.setup(BanMiddleware(bot))
