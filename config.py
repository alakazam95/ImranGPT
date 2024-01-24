from aiogram import Bot, Dispatcher
from subscribe_checker import BanMiddleware
import os


script_dir = os.path.dirname(os.path.abspath(__file__))

# Создаем относительный путь к файлу базы данных относительно директории скрипта
DATABASE_PATH = os.path.join(script_dir, "data", "mydatabase.db")

bot = Bot(token='6727239369:AAFxy9hXV14G3bjXrj6CXC2Rt4LMFUbyiXA')
dp = Dispatcher(bot)
dp.middleware.setup(BanMiddleware(bot))
