import os
import random
import qrcode
from PIL import Image, ImageDraw, ImageFont
from pyzbar.pyzbar import decode
from pathlib import Path
from random import randint

from config import PHRASES, BASE_DIR, COUPON_CODES_FILE
from module.TinyDB.function import update_user, get_user

QR_DIR = os.path.join(BASE_DIR, 'data', 'QR')
QR_TEMPLATE = os.path.join(QR_DIR, 'Template')
QR_TEMP = os.path.join(QR_DIR, 'Temp')

async def generate_qr_code_with_template(user_id, bot):
    progress_message = await bot.send_message(user_id, PHRASES["generating_qr"])
    
    user = get_user(user_id)

    selected_code = user['CouponCode']

    # Генерация QR-кода с использованием функции из CouponGen.py
    qr = gen_qr_code(selected_code)

    # Путь к шаблону
    template_files = [file_name for file_name in os.listdir(QR_TEMPLATE) if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

    if not template_files:
        raise FileNotFoundError("No template image found in QR_TEMPLATE.")
    
    template_image_path = max(
        (os.path.join(QR_TEMPLATE, file_name) for file_name in template_files),
        key=os.path.getmtime
    )

    template_img = Image.open(template_image_path).convert("RGBA")

    # Размеры QR-кода
    qr_xy = (60, 810)
    qr_width, qr_height = qr.size
    fontcords = (qr_xy[0] + qr_width / 2, qr_xy[1] + qr_width + 3)

    # Наложение QR-кода на шаблон
    alpha = Image.new('RGBA', (qr_width, qr_width), (255, 255, 255, int(255 * 0.40)))
    template_img.paste(alpha, qr_xy, alpha)
    template_img.paste(qr, qr_xy, qr)

    # Добавление текста на изображение
    drawNumber(template_img, selected_code, fontcords, size=60, spacing=5)

    # Сохранение изображения
    template_extension = os.path.splitext(template_image_path)[1]  
    save_format = template_extension[1:].upper()

    if save_format in ('JPG', 'JPEG'):
        save_format = 'JPEG'
        template_img = template_img.convert("RGB")
    
    temp_output_path = os.path.join(QR_TEMP, f"output_{user_id}{template_extension}")
    template_img.save(temp_output_path, format=save_format) 

    # Отправка изображения пользователю
    with open(temp_output_path, "rb") as file:
        sent_message = await bot.send_photo(chat_id=user_id, photo=file) 
        file_id = sent_message.photo[-1].file_id

    update_user(user_id, CouponIMG=file_id)

    os.remove(temp_output_path)

    await bot.delete_message(user_id, progress_message.message_id)

    return selected_code

# Функция для генерации QR-кода из CouponGen.py
def gen_qr_code(text: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.get_matrix()

    coeff = 9                           #размер qr кода
    coeff_small = coeff / (300 / 100)   #размер кубиков 
    length_qr = len(img) * coeff

    output_qr = Image.new('RGBA', (length_qr, length_qr), (0, 0, 0, 0))
    
    black_1 = (0, 0, 0, 0)
    black_2 = (0, 0, 0, 230)
    white_1 = (255, 255, 255, 50)
    white_2 = (255, 255, 255, 230)

    white_3 = (0, 0, 0, 0)

    idraw = ImageDraw.Draw(output_qr, "RGBA")
    
    x = 0
    y = 0
    for string in qr.get_matrix():
        this_str = ''
        for i in string:
            if i:
                this_str += '1'
                idraw.rectangle((x + coeff_small, y + coeff_small, x + coeff - coeff_small, y + coeff - coeff_small),
                                fill=black_2)
            else:
                this_str += '0'
                idraw.rectangle((x + coeff_small, y + coeff_small, x + coeff - coeff_small, y + coeff - coeff_small),
                                fill=white_2)
            x += coeff
        x = 0
        y += coeff
        
    idraw.rectangle((0, 0, coeff * 9, coeff * 9), fill=white_1)
    idraw.rectangle((length_qr - coeff * 9, 0, length_qr, coeff * 9), fill=white_1)
    idraw.rectangle((0, length_qr - coeff * 9, coeff * 9, length_qr), fill=white_1)
    idraw.rectangle((length_qr - coeff * 10, length_qr - coeff * 9, length_qr - coeff * 6, length_qr - coeff * 6),
                    fill=white_1)
                    
    idraw.rectangle((coeff, coeff, coeff * 8, coeff * 2), fill=black_2)
    idraw.rectangle((length_qr - coeff * 8, coeff, length_qr - coeff, coeff * 2), fill=black_2)
    idraw.rectangle((coeff, coeff * 7, coeff * 8, coeff * 8), fill=black_2)
    idraw.rectangle((length_qr - coeff * 8, coeff * 7, length_qr - coeff, coeff * 8), fill=black_2)
    idraw.rectangle((coeff, length_qr - coeff * 8, coeff * 8, length_qr - coeff * 7), fill=black_2)
    idraw.rectangle((coeff, length_qr - coeff * 2, coeff * 8, length_qr - coeff), fill=black_2)
    idraw.rectangle((length_qr - coeff * 8, length_qr - coeff * 8, length_qr - coeff * 7, length_qr - coeff * 7),
                    fill=black_2)
    idraw.rectangle((coeff * 3, coeff * 3, coeff * 6, coeff * 6), fill=black_2)
    idraw.rectangle((length_qr - coeff * 6, coeff * 3, length_qr - coeff * 3, coeff * 6), fill=black_2)
    idraw.rectangle((coeff * 3, length_qr - coeff * 6, coeff * 6, length_qr - coeff * 3), fill=black_2)
    idraw.rectangle((coeff, coeff, coeff * 2, coeff * 8), fill=black_2)
    idraw.rectangle((coeff * 7, coeff, coeff * 8, coeff * 8), fill=black_2)

    idraw.rectangle((length_qr - coeff * 2, coeff, length_qr - coeff, coeff * 8), fill=black_2)
    idraw.rectangle((length_qr - coeff * 8, coeff, length_qr - coeff * 7, coeff * 8), fill=black_2)

    idraw.rectangle((coeff, length_qr - coeff * 8, coeff * 2, length_qr - coeff), fill=black_2)
    idraw.rectangle((coeff * 7, length_qr - coeff * 8, coeff * 8, length_qr - coeff), fill=black_2)

    idraw.rectangle((length_qr - coeff * 10, length_qr - coeff * 10, length_qr - coeff * 9, length_qr - coeff * 5),
                    fill=black_2)
    idraw.rectangle((length_qr - coeff * 6, length_qr - coeff * 10, length_qr - coeff * 5, length_qr - coeff * 5),
                    fill=black_2)

    idraw.rectangle((length_qr - coeff * 10, length_qr - coeff * 10, length_qr - coeff * 6, length_qr - coeff * 9),
                    fill=black_2)
    idraw.rectangle((length_qr - coeff * 10, length_qr - coeff * 6, length_qr - coeff * 6, length_qr - coeff * 5),
                    fill=black_2)
    return output_qr

def drawNumber(img, s, xy=(0, 0), size=58, spacing=5):
    # Используем стандартный шрифт Arial
    try:
        font = ImageFont.truetype("arial.ttf", size)
    except IOError:
        # Если Arial недоступен, используем шрифт по умолчанию
        font = ImageFont.load_default()
        print("Шрифт arial.ttf не найден. Используется шрифт по умолчанию.")
    
    idraw = ImageDraw.Draw(img, "RGBA")
    
    # Добавляем межбуквенный интервал
    spaced_text = " ".join(s)  # Добавляем пробелы между символами
    idraw.text(xy, spaced_text, (255, 255, 255, 88), anchor="mt", font=font)

def save_coupon_code(user_id, phone_number):
    txt_file_path = os.path.join(QR_DIR, COUPON_CODES_FILE)
    
    if not os.path.exists(txt_file_path):
        raise FileNotFoundError("The codes.txt file is missing in QR_DIR.")

    with open(txt_file_path, 'r') as file:
        codes = file.readlines()

    codes = [code.strip() for code in codes if code.strip()]

    if not codes:
        update_user(user_id, phone_number=phone_number, CouponCode=None)
        return None

    selected_code = random.choice(codes)

    codes.remove(selected_code)

    with open(txt_file_path, 'w') as file:
        file.writelines(f"{code}\n" for code in codes)

    update_user(user_id, phone_number=phone_number, CouponCode=selected_code)

    return selected_code

async def send_coupon(user_id, chat_id, bot):
    user = get_user(user_id)
    if not user:
        raise ValueError("User not found in the database.")

    if 'CouponIMG' in user:
        file_id = user['CouponIMG']
        try:
            await bot.send_photo(chat_id, file_id)
            return 
        except Exception as e:
            pass

    if 'CouponCode' not in user or user['CouponCode'] is None:
        phone_number = user.get('phone_number', None) 

        selected_code = save_coupon_code(user_id, phone_number)

        if selected_code is None:
            await bot.send_message(chat_id, PHRASES["none_CouponCode"])
            return  

    await generate_qr_code_with_template(user_id, bot)

    return