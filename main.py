from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import dp
import handlers.start
import handlers.callback_handlers

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
