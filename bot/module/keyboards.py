from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import PHRASES

keyboard_start = ReplyKeyboardMarkup(resize_keyboard=True)
btn_back = KeyboardButton('Кнопка 1')
keyboard_start.add(btn_back)

request_phone_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
request_phone_keyboard.add(KeyboardButton(PHRASES["btn_share_phone"], request_contact=True))

back_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
btn_back = KeyboardButton('Назад')
back_menu_keyboard.add(btn_back)

keyboard_admin = ReplyKeyboardMarkup(resize_keyboard=True)
users_admin = KeyboardButton('Выгрузить список телефонов')
keyboard_admin.add(users_admin)


def get_skip_cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(PHRASES["btn_skip"]), KeyboardButton(PHRASES["btn_cancel"]))
    return keyboard

def get_skip_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(PHRASES["btn_skip"]))
    return keyboard

def get_cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(PHRASES["btn_cancel"]))
    return keyboard
