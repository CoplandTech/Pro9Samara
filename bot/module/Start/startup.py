import asyncio
from aiogram.types import BotCommand

from loader import bot

from module.Start.user import remind_birth_date  

async def on_startup(_):
    await bot.set_my_commands([
        BotCommand("start", "Начать/Вернуться к началу"),
        BotCommand("admin", "потом удалить")
    ])
    asyncio.create_task(remind_birth_date()) # Запускаем напоминания