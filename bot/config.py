import os

API_TOKEN = 'TOKEN'

ADMINS = ['ADM1', 'ADM2']

DELAY_BIRTH_DAY_MESSAGES = 0 # Интервал отправки уведомления о указании ДР

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

QR_DIR = os.path.join(BASE_DIR, 'data', 'QR')
QR_TEMPLATE = os.path.join(QR_DIR, 'Template')


PHRASES = {
    "registered": "Привет, мы Вас помним, вот Ваш купон!",
    "request_user_phone": "Пожалуйста, отправьте ваш номер телефона, используя кнопку.",
    "user_sender_phone": "Спасибо!\nУкажите вашу дату рождения в формате ДД.ММ.ГГГГ.\nЕсли не хотите указывать дату рождения, или пропустите этот шаг.",
    "skip_send_birth": "Дата рождения пропущена. Вот ваш купон!",
    "user_sender_phone_birth": "Спасибо! Регистрация завершена. Выберите действие:",

    "error_user_birth": "Некорректный формат даты, отправьте текст в формате ДД.ММ.ГГГГ или пропустите этот шаг.",

    "notification_send_birth": "Напоминаем, что вы не указали дату рождения.\nПожалуйста, укажите её в формате ДД.ММ.ГГГГ или пропустите этот шаг.",

    "btn_share_phone": "Поделиться 📱",
    "btn_skip": "Пропустить ⏩",
    "btn_cancel": "Отменить ❌",

}


# ---- NO USLES ----
DAYS_INACTIVE_THRESHOLD = 7  # Количество дней для проверки неактивности
REMINDER_CHECK_INTERVAL = 86400  # Интервал проверки в секундах

PAGE_SIZE_USER = 2 # Количество элементов пользователей - админ
PAGE_SIZE_REQS = 5 # Количество элементов запросов - админ
PAGE_SIZE_POSTS = 5 # Количество элементов ПОЛЕЗНОЕ и ПОСТЫ - админ

PAGE_SIZE_TOOLS = 3 # Количество элементов ПОЛЕЗНОЕ - юзер
