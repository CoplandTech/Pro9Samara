from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType
from datetime import datetime, timedelta
import asyncio

from loader import dp
from config import PHRASES, DELAY_BIRTH_DAY_MESSAGES
from module.keyboards import keyboard_start, request_phone_keyboard, get_skip_keyboard
from module.TinyDB.config import db_users

from module.TinyDB.function import create_user, update_user, is_registration_complete
from module.utils import validate_date_format

@dp.message_handler(commands=['start'])
async def start_command_handler(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or None
    full_name = message.from_user.full_name or None

    create_user(user_id, username, full_name)

    if is_registration_complete(user_id):
        update_user(user_id, last_active=datetime.now().isoformat())
        await message.answer(PHRASES["registered"], reply_markup=keyboard_start)
    else:
        await message.answer(PHRASES["request_user_phone"], reply_markup=request_phone_keyboard)
        await dp.storage.set_state(chat=message.chat.id, user=message.from_user.id, state="awaiting_phone")

@dp.message_handler(state="awaiting_phone", content_types=ContentType.ANY)
async def contact_handler(message: types.Message):
    user_id = message.from_user.id

    if message.content_type != ContentType.CONTACT or not hasattr(message, 'contact') or message.contact.user_id != user_id:
        await message.answer(PHRASES["request_user_phone"], reply_markup=request_phone_keyboard)
        return

    phone_number = message.contact.phone_number
    update_user(user_id, phone_number=phone_number)

    await message.answer(PHRASES["user_sender_phone"], reply_markup=get_skip_keyboard())
    await dp.storage.set_state(chat=message.chat.id, user=user_id, state="awaiting_birth_date")


@dp.message_handler(state="awaiting_birth_date", content_types=ContentType.ANY)
async def birth_date_handler(message: types.Message):
    user_id = message.from_user.id

    if message.content_type != ContentType.TEXT:
        await message.answer(PHRASES["error_user_birth"], reply_markup=get_skip_keyboard())
        return

    birth_date = message.text.strip()

    if birth_date == (PHRASES["btn_skip"]):
        await message.answer(PHRASES["skip_send_birth"], reply_markup=keyboard_start)
        await dp.storage.reset_state(chat=message.chat.id, user=user_id)
        return

    if validate_date_format(birth_date):
        update_user(user_id, birth_date=birth_date)
        await message.answer(PHRASES["user_sender_phone_birth"], reply_markup=keyboard_start)
        await dp.storage.reset_state(chat=message.chat.id, user=user_id)
    else:
        await message.answer(PHRASES["error_user_birth"], reply_markup=get_skip_keyboard())
    
@dp.message_handler(Text(equals="Кнопка 1"))
async def button_1_handler(message: types.Message):
    await message.answer("Ахахахах")

async def remind_birth_date():
    if DELAY_BIRTH_DAY_MESSAGES == 0:
        return 
    
    while True:
        now = datetime.now()
        for user in db_users.all():
            user_id = user['id']
            last_active = datetime.fromisoformat(user.get('last_active'))
            if not user.get('birth_date') and (now - last_active > timedelta(minutes=2)):
                try:
                    await dp.bot.send_message(user_id, PHRASES["notification_send_birth"], reply_markup=get_skip_keyboard())
                    await dp.storage.set_state(chat=user_id, user=user_id, state="awaiting_birth_date")
                except Exception as e:
                    print(f"Ошибка отправки пользователю {user_id}: {e}")
        await asyncio.sleep(DELAY_BIRTH_DAY_MESSAGES)