import logging
from aiogram.utils import executor

from loader import dp
from module.Start.startup import on_startup

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, allowed_updates=["message", "callback_query"])
