from aiogram.utils import executor
from config import dp
from aiogram import types
import data.creator as db
from config import bot, dp
from data.subscription import valid_subscriptions
from handlers import mode
import handlers.mode
import handlers.myid
import handlers.profile
import handlers.start
import handlers.pay
import handlers.callback_handlers
import AI.midj_logic





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
