from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import dp
from config import ADMINS
from module.keyboards import keyboard_admin

class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message):
        return str(message.from_user.id) in ADMINS
    
dp.filters_factory.bind(AdminFilter)
    
@dp.message_handler(commands=['admin'], is_admin=True)
async def admin(message: types.Message):
    await message.answer(text="Вы авторизированы!", reply_markup=keyboard_admin)