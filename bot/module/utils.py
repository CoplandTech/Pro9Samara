import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import BoundFilter
from datetime import datetime

from loader import dp
from config import ADMINS

logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message):
        return str(message.from_user.id) in ADMINS
    
dp.filters_factory.bind(AdminFilter)

# --- Валидация даты ---
def validate_date_format(date_text):
    try:
        birth_date = datetime.strptime(date_text, "%d.%m.%Y")
        
        today = datetime.now().date()
        
        if birth_date.date() > today:
            return False
        return True
    except ValueError:
        return False

async def handle_pagination(callback_query: types.CallbackQuery, state: FSMContext, list_function, page_size: int, prefix: str):
    data = callback_query.data
    
    if data.startswith(f"prev_page_{prefix}_") or data.startswith(f"next_page_{prefix}_"):
        _, _, _, page = data.split("_")
        page = int(page)
        
        await list_function(callback_query.message, state, page, edit=True)
        await callback_query.answer()


# @dp.message_handler()
# async def handle_unexpected_message(message: types.Message, state: FSMContext):
#     await message.answer("Мы пока не хотим принимать простые сообщения 😶")