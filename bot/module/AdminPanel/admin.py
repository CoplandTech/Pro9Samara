from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import logging
import datetime

from loader import dp, bot
from config import PAGE_SIZE_USER
# from module.keyboards import keyboard_admin
from module.utils import handle_pagination

from module.TinyDB.config import Query, db_users
from module.AdminPanel.states import AdminPanelState

logging.basicConfig(level=logging.INFO)

@dp.message_handler(Text(equals='Выгрузить список телефонов'), is_admin=True)
async def phone_user_list(message: types.Message, state: FSMContext, page: int = 1, edit: bool = False):
    users = db_users.all()
    
    if not users:
        await message.answer("Пользователей нет в базе.")
        return

    total_pages = (len(users) + PAGE_SIZE_USER - 1) // PAGE_SIZE_USER
    start_index = (page - 1) * PAGE_SIZE_USER
    end_index = start_index + PAGE_SIZE_USER
    users_to_show = users[start_index:end_index]

    current_data = await state.get_data()
    text_messages = current_data.get('text_messages_users', [])
    
    for message_id in text_messages:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
        except Exception as e:
            print(f"Ошибка при удалении сообщения {message_id}: {e}")

    new_text_messages = []

    for user in users_to_show:
        date_added = datetime.datetime.fromisoformat(user['date_added']).strftime('%d.%m.%Y в %H:%M')
        last_active = datetime.datetime.fromisoformat(user['last_active']).strftime('%d.%m.%Y в %H:%M')

        user_info = f"ID: {user['id']}\n<a href='tg://user?id={user['id']}'>{user['full_name']}</a>, зарегистрирован {date_added}.\nПоследняя активность {last_active}"

        # Вывод номера телефона, если он есть
        if user.get('phone_number'):
            user_info += f"\n\nНомер телефона: {user['phone_number']}"

        sent_message = await message.answer(user_info, parse_mode="HTML")
        new_text_messages.append(sent_message.message_id)

    await state.update_data(text_messages_users=new_text_messages)

# @dp.message_handler(Text(equals='Назад'), state=[AdminPanelState.publications, AdminPanelState.reqs])
# async def go_back(message: types.Message, state: FSMContext):
#     await AdminPanelState.activ.set()
#     await message.answer("Выбери действие: ", reply_markup=keyboard_admin)