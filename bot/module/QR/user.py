import os
import random
import qrcode
from PIL import Image, ImageDraw, ImageFont

from config import PHRASES, BASE_DIR, COUPON_CODES_FILE
from module.TinyDB.function import update_user, get_user

QR_DIR = os.path.join(BASE_DIR, 'data', 'QR')
QR_TEMPLATE = os.path.join(QR_DIR, 'Template')
QR_TEMP = os.path.join(QR_DIR, 'Temp')

async def generate_qr_code_with_template(user_id, bot):
    progress_message = await bot.send_message(user_id, PHRASES["generating_qr"])
    
    user = get_user(user_id)

    selected_code = user['CouponCode']

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    qr.add_data(selected_code)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    template_files = [file_name for file_name in os.listdir(QR_TEMPLATE) if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

    if not template_files:
        raise FileNotFoundError("No template image found in QR_TEMPLATE.")
    
    template_image_path = max(
        (os.path.join(QR_TEMPLATE, file_name) for file_name in template_files),
        key=os.path.getmtime
    )

    template_img = Image.open(template_image_path).convert("RGBA")

    qr_img = qr_img.resize((300, 300))
    template_img.paste(qr_img, (50, 50), qr_img)

    template_extension = os.path.splitext(template_image_path)[1]  
    save_format = template_extension[1:].upper()

    if save_format in ('JPG', 'JPEG'):
        save_format = 'JPEG'
        template_img = template_img.convert("RGB")
    
    temp_output_path = os.path.join(QR_TEMP, f"output_{user_id}{template_extension}")
    template_img.save(temp_output_path, format=save_format) 

    with open(temp_output_path, "rb") as file:
        sent_message = await bot.send_photo(chat_id=user_id, photo=file) 
        file_id = sent_message.photo[-1].file_id

    update_user(user_id, CouponIMG=file_id)

    os.remove(temp_output_path)

    await bot.delete_message(user_id, progress_message.message_id)

    return selected_code

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