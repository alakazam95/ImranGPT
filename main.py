from aiogram.utils import executor
from config import dp
from aiogram import types
import data.creator as db
from config import bot, dp
from data.subscription import valid_subscriptions
from data.sub_manager import SubscriptionManager

from aiogram.utils import executor
from config import dp
from aiogram import types
from config import bot, dp
from data.subscription import valid_subscriptions
from handlers import mode
import handlers.mode
import handlers.myid
import handlers.profile
import handlers.start
import handlers.help
import handlers.pay
import handlers.reset
import handlers.callback_handlers
import AI.midj_logic
import AI.gpt_logic


# Создаем экземпляр DBManager
db_manager = db.DBManager()

# Создаем экземпляр SubscriptionManager, передаем ему db_manager
sub_manager = SubscriptionManager(db_manager)

if __name__ == '__main__':
    sub_manager.start()

    executor.start_polling(dp, skip_updates=True)
