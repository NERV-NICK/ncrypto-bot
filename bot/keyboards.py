from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import WebAppInfo

import os
import dotenv

dotenv.load_dotenv()

game = (
    InlineKeyboardBuilder()
    .button(text="Open game", web_app=WebAppInfo(url=f"{os.getenv('URL')}"))
).as_markup()


admin = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Users List")],
        [KeyboardButton(text="Give $NCOIN")],
        [KeyboardButton(text="Bun User")],
        [KeyboardButton(text="Get User")]],
    resize_keyboard=True,
    input_field_placeholder="Select admin cmd..."
)