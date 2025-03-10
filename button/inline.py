from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def direction_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Frontend", callback_data="frontend"),
         InlineKeyboardButton(text="Backend", callback_data="backend")],
        [InlineKeyboardButton(text="Flutter dasturchi", callback_data="flutter"),
         InlineKeyboardButton(text="Sotuv menejeri", callback_data="sales")],
        [InlineKeyboardButton(text="⬅️ Ortga", callback_data="back")]
    ])
    return keyboard

