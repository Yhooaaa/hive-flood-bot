from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="отправить заявку")],
    ],
    resize_keyboard=True
)
