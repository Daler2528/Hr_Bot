from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def reply_net_link():
    rkb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Ariza qoldirish ✅")],
        ],
        resize_keyboard=True  # Tugmalar ekranga moslashishi uchun
    )
    return rkb

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

confirm_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Davom etish ▶️")]],
    resize_keyboard=True
)



def phone_request_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True  # Tugmalar faqat bir marta ko‘rinadi
    )
