# ---- Напиши код для генерации QR без сохранения в Папку, а кодирование в base64, чтобы сразу записывать в БД ----
# ---- Напиши код для генерации QR без сохранения в Папку, а кодирование в base64, чтобы сразу записывать в БД ----
# ---- Напиши код для генерации QR без сохранения в Папку, а кодирование в base64, чтобы сразу записывать в БД ----
# ---- Напиши код для генерации QR без сохранения в Папку, а кодирование в base64, чтобы сразу записывать в БД ----


Вот примеры:


import random
from pathlib import Path
from PIL import Image
from io import BytesIO
from aiogram.types import InputFile

from module.TinyDB.config import Query, db_users

from config import QR_DIR, QR_TEMPLATE

# Проверяем наличие шаблона
def get_template_path():
    allowed_extensions = ["png", "jpg", "jpeg", "webp"]
    for ext in allowed_extensions:
        template_path = Path(QR_TEMPLATE).joinpath(f"pro9.{ext}")
        if template_path.exists():
            return str(template_path)
    raise FileNotFoundError("Шаблон купона не найден в папке QR_TEMPLATE.")

# Получаем случайный код купона из файла
def get_random_coupon_code():
    codes_path = Path(QR_DIR).joinpath("CouponCodes.txt")
    if not codes_path.exists():
        raise FileNotFoundError("Файл CouponCodes.txt не найден.")
    
    with open(codes_path, "r", encoding="utf-8") as file:
        codes = [line.strip() for line in file if line.strip()]

    if not codes:
        raise ValueError("Файл CouponCodes.txt пуст.")

    selected_code = random.choice(codes)

    # Удаляем использованный код из файла
    with open(codes_path, "w", encoding="utf-8") as file:
        file.writelines([code + "\n" for code in codes if code != selected_code])
    
    return selected_code


# Сохраняем купон в базе и отправляем пользователю
async def assign_coupon_to_user(user_id):
    try:
        # Получаем шаблон и случайный код купона
        template_path = get_template_path()
        coupon_code = get_random_coupon_code()

        # Генерируем временное изображение купона
        temp_dir = Path(QR_DIR).joinpath("Temp")
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_path = temp_dir.joinpath(f"{coupon_code}.jpg")

        # Генерация купона
        createCoupon(coupon_code)

        # Кодируем изображение в строку для сохранения в базу
        with open(temp_path, "rb") as img_file:
            encoded_image = img_file.read().hex()

        # Сохраняем купон в базу данных
        db_users.update({
            "CouponCodes": coupon_code,
            "TemplateCoupon": encoded_image
        }, Query().id == user_id)

        # Удаляем временный файл
        temp_path.unlink()
        return coupon_code
    except Exception as e:
        raise Exception(f"Ошибка при создании купона: {e}")

# Генерация купона и сохранение в базу
async def generate_coupon_for_user(user_id):
    try:
        # Генерация купона без отправки
        await assign_coupon_to_user(user_id)
        print(f"Купон успешно сгенерирован для пользователя {user_id}.")
    except Exception as e:
        print(f"Ошибка при генерации купона для пользователя {user_id}: {e}")

# Отправка купона из базы
async def send_coupon_from_db(user_id, chat_id):
    try:
        user_data = db_users.get(Query().id == user_id)
        coupon_code = user_data.get("CouponCodes")
        encoded_image = user_data.get("TemplateCoupon")

        if not coupon_code or not encoded_image:
            await dp.bot.send_message(chat_id, "Купон не найден.")
            return

        # Декодируем изображение из базы
        image_data = BytesIO(bytes.fromhex(encoded_image))
        image_data.seek(0)  # Устанавливаем указатель в начало потока

        # Отправляем изображение
        await dp.bot.send_photo(chat_id, photo=InputFile(image_data, filename=f"{coupon_code}.jpg"), caption="Ваш купон успешно создан!")
    except Exception as e:
        await dp.bot.send_message(chat_id, f"Ошибка при отправке купона: {e}")



# ---- Напиши код для генерации QR без сохранения в Папку, а кодирование в base64, чтобы сразу записывать в БД ----
# ---- Напиши код для генерации QR без сохранения в Папку, а кодирование в base64, чтобы сразу записывать в БД ----
# ---- Напиши код для генерации QR без сохранения в Папку, а кодирование в base64, чтобы сразу записывать в БД ----
# ---- Напиши код для генерации QR без сохранения в Папку, а кодирование в base64, чтобы сразу записывать в БД ----