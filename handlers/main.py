
import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html , F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, CallbackQuery

from button.inline import direction_keyboard
from button.replay import reply_net_link, phone_request_keyboard

# Bot token can be obtained via https://t.me/BotFather
from dotenv import load_dotenv
load_dotenv()
TOKEN = getenv('TOKEN')

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


class Form(StatesGroup):
    phone_number = State() # Telefon raqami uchun holat
    name = State()
    direction = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Assalomu alaykum.\n\nHozirda bizda Backend, Frontend, Flutter va Sotuv menejerlariga talab bor.\n\nAriza qoldirish uchun pastdagi `Ariza qoldirish` ni bosing." , reply_markup=reply_net_link())


@dp.message(F.text == "Ariza qoldirish ✅")
async def ask_phone_number(message: Message, state: FSMContext):
    await message.answer("Iltimos, pastdagi tugma orqali telefon raqamingizni yuboring 📲",
                         reply_markup=phone_request_keyboard())
    await state.set_state(Form.phone_number)  # FSM-ni telefon raqami holatiga o'tkazamiz


@dp.message(F.contact)
async def save_phone_number(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number  # Telefon raqamni olish
    await state.update_data(phone_number=phone_number)  # State ichiga saqlaymiz

    await message.answer(f"Ismingizni yuboring ✍️")
    await state.set_state(Form.name)



@dp.message(Form.name)
async def save_full_name(message: Message, state: FSMContext):
    """Ismni saqlaymiz va yo‘nalishni tanlash tugmalarini chiqaramiz"""
    name = message.text
    await state.update_data(name=name)

    await message.answer("📌 Endi o‘zingizga mos yo‘nalishni tanlang:",
                         reply_markup=direction_keyboard())

    await state.set_state(Form.direction)


@dp.callback_query(Form.direction)
async def save_direction(callback: CallbackQuery, state: FSMContext):
    """Yo‘nalishni saqlaymiz va hamma ma'lumotlarni tasdiqlaymiz"""
    direction_map = {
        "frontend": "Frontend",
        "backend": "Backend",
        "flutter": "Flutter dasturchi",
        "sales": "Sotuv menejeri"
    }

    direction = callback.data
    if direction == "back":
        await callback.message.answer("⬅️ Ortga qaytish")
        await state.clear()
        return

    await state.update_data(direction=direction_map.get(direction, "Noma'lum yo‘nalish"))

    user_data = await state.get_data()
    phone = user_data.get("phone_number")
    name = user_data.get("name")
    chosen_direction = user_data.get("direction")

    await callback.message.answer(f"✅ Ma'lumotlar saqlandi!\n\n"
                                  f"📞 Telefon: {phone}\n"
                                  f"👤 Ism: {name}\n"
                                  f"🛠 Yo‘nalish: {chosen_direction}")

    await state.clear()

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())