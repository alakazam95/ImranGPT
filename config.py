from aiogram import Bot, Dispatcher
from subscribe_checker import BanMiddleware
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

script_dir = os.path.dirname(os.path.abspath(__file__))

DATABASE_PATH = os.path.join(script_dir, "data", "mydatabase.db")
OPENAI_API_KEY = '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'

storage = MemoryStorage()

bot = Bot(token='6727239369:AAFxy9hXV14G3bjXrj6CXC2Rt4LMFUbyiXA')
dp = Dispatcher(bot, storage= storage)
dp.middleware.setup(BanMiddleware(bot))


MID_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTAzOTAsImVtYWlsIjoibWFtb250c2xvbm92QGdtYWlsLmNvbSIsInVzZXJuYW1lIjoibWFtb250c2xvbm92QGdtYWlsLmNvbSIsImlhdCI6MTcwNzU5MzYxNH0.U1_DgEwZkJ4u6l3NnDuTecIsFqvAxnrqnnY3o7bthwc"
