import os
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp, bot
from config import PHRASES, COUPON_CODES_FILE
from module.keyboards import get_cancel_keyboard, keyboard_admin

from module.utils import AdminFilter
from module.QR.user import QR_DIR, QR_TEMPLATE

class TemplateStates(StatesGroup):
    awaiting_template = State()

class CouponStates(StatesGroup):
    awaiting_coupons = State()

@dp.message_handler(Text(equals=PHRASES["btn_coupons_admin"]), is_admin=True)
async def coupons_admin_menu(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(
        InlineKeyboardButton(PHRASES["btn_show_template_coupons"], callback_data="show_template_coupons"),
    )
    keyboard.add(
        InlineKeyboardButton(PHRASES["btn_import_coupons"], callback_data="import_coupons"),
        InlineKeyboardButton(PHRASES["btn_export_coupons"], callback_data="export_coupons")
    )

    await message.answer(PHRASES["change_action"], reply_markup=keyboard)

@dp.callback_query_handler(Text(equals="show_template_coupons"))
async def show_template_coupons(callback_query: types.CallbackQuery):
    try:
        files = sorted(os.listdir(QR_TEMPLATE), key=lambda x: os.path.getmtime(os.path.join(QR_TEMPLATE, x)), reverse=True)
        if files:
            newest_file = os.path.join(QR_TEMPLATE, files[0])
            with open(newest_file, 'rb') as file:
                keyboard = InlineKeyboardMarkup().add(
                    InlineKeyboardButton(PHRASES["btn_replace_template"], callback_data="replace_template")
                )
                await callback_query.message.answer_document(file, reply_markup=keyboard)
        else:
            await callback_query.message.answer(PHRASES["error_not_found_template"])
    except Exception as e:
        await callback_query.message.answer(f"Ошибка при загрузке шаблона: {str(e)}")

@dp.callback_query_handler(Text(equals="replace_template"))
async def replace_template(callback_query: types.CallbackQuery, state: FSMContext):
    await TemplateStates.awaiting_template.set()
    await callback_query.message.answer(PHRASES["send_template_admin"], reply_markup=get_cancel_keyboard())

@dp.message_handler(state=TemplateStates.awaiting_template, content_types=types.ContentType.ANY)
async def handle_template_upload(message: types.Message, state: FSMContext):
    if message.text == PHRASES["btn_cancel"]:
        await cancel_action(message, state)
        return
    
    if not message.document:
        await message.answer(PHRASES["error_template_not_doc"])
        return
    
    file_extension = os.path.splitext(message.document.file_name)[1].lower()
    if file_extension not in [".webp", ".jpg", ".jpeg", ".png"]:
        await message.answer(PHRASES["error_template_not_doc"])
        return

    file_path = os.path.join(QR_TEMPLATE, message.document.file_name)
    os.makedirs(QR_TEMPLATE, exist_ok=True)

    for file in os.listdir(QR_TEMPLATE):
        os.remove(os.path.join(QR_TEMPLATE, file))

    await message.document.download(destination_file=file_path)
    await message.answer(PHRASES["success_replace_template"], reply_markup=keyboard_admin)
    await state.finish()

@dp.callback_query_handler(Text(equals="export_coupons"))
async def export_coupons(callback_query: types.CallbackQuery):
    file_path = os.path.join(QR_DIR, COUPON_CODES_FILE)
    try:
        with open(file_path, 'rb') as file:
            await callback_query.message.answer_document(file)
    except FileNotFoundError:
        await callback_query.message.answer(PHRASES["error_not_found_coupons"])

@dp.callback_query_handler(Text(equals="import_coupons"))
async def import_coupons(callback_query: types.CallbackQuery, state: FSMContext):
    await CouponStates.awaiting_coupons.set()
    await callback_query.message.answer(PHRASES["sent_coupons_file"], reply_markup=get_cancel_keyboard())

@dp.message_handler(state=CouponStates.awaiting_coupons, content_types=types.ContentType.ANY)
async def handle_coupons(message: types.Message, state: FSMContext):
    if message.text == PHRASES["btn_cancel"]:
        await cancel_action(message, state)
        return

    if message.document:
        file_extension = os.path.splitext(message.document.file_name)[1].lower()
        if file_extension != ".txt":
            await message.answer(PHRASES["error_coupons_txt"])
            return

        file_path = os.path.join(QR_DIR, COUPON_CODES_FILE)
        os.makedirs(QR_DIR, exist_ok=True)

        try:
            if os.path.exists(file_path):
                os.remove(file_path)

            await message.document.download(destination_file=file_path)
            await message.answer(PHRASES["success_replase_coupons"], reply_markup=keyboard_admin)
            await state.finish()
        except Exception as e:
            await message.answer(f"Ошибка при загрузке файла: {str(e)}")
        return

    if message.text:
        file_path = os.path.join(QR_DIR, COUPON_CODES_FILE)
        os.makedirs(QR_DIR, exist_ok=True)

        try:
            with open(file_path, 'a', encoding='utf-8') as file:
                coupons = message.text.splitlines()
                file.writelines([f"{coupon}\n" for coupon in coupons if coupon.strip()])
            await message.answer(PHRASES["success_replase_coupons"], reply_markup=keyboard_admin)
            await state.finish()
        except Exception as e:
            await message.answer(f"Ошибка при сохранении купонов: {str(e)}")
        return

    await message.answer(PHRASES["sent_coupons_file"])

@dp.message_handler(Text(equals=PHRASES["btn_cancel"]), state=[TemplateStates.awaiting_template, CouponStates.awaiting_coupons])
async def cancel_action(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(PHRASES["action_cancel"], reply_markup=keyboard_admin)