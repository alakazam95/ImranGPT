from aiogram.utils import executor
from config import dp
import handlers.profile
import handlers.callback_handlers
import handlers.pay
import handlers.start
import mode
import handlers.reset
import handlers.img
import handlers.help
import handlers.blend
import handlers.ask
from AI import gpt_logic
from handlers import myid



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

