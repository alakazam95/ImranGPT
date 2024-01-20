from aiogram import Bot, Dispatcher
from subscribe_checker import BanMiddleware

API_TOKEN = 'Ваш_Telegram_токен'

bot = Bot(token='6727239369:AAFxy9hXV14G3bjXrj6CXC2Rt4LMFUbyiXA')
dp = Dispatcher(bot)
dp.middleware.setup(BanMiddleware(bot))
