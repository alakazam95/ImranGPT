from aiogram.utils import executor
from config import dp
from handlers import mode
import handlers.mode
import handlers.callback_handlers
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
