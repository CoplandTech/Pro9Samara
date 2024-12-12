from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import PHRASES

#---- BTNS ----

btn_back = KeyboardButton(PHRASES["btn_back"])
btn_get_coupon = KeyboardButton(PHRASES["btn_get_coupon"])
btn_cancel = KeyboardButton(PHRASES["btn_cancel"])
btn_skip = KeyboardButton(PHRASES["btn_skip"])


btn_users_admin = KeyboardButton(PHRASES["btn_users_admin"])
btn_coupons_admin = KeyboardButton(PHRASES["btn_coupons_admin"])

#---- KEYBOARDS ----

keyboard_start = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_start.add(btn_get_coupon)

request_phone_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
request_phone_keyboard.add(KeyboardButton(PHRASES["btn_share_phone"], request_contact=True))

back_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
back_menu_keyboard.add(btn_back)

keyboard_admin = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_admin.add(btn_users_admin, btn_coupons_admin).add(btn_back)

def get_skip_cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(btn_skip, btn_cancel)
    return keyboard

def get_skip_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(btn_skip)
    return keyboard

def get_cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(btn_cancel)
    return keyboard
