import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters.command import CommandStart
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import keybord as kb
from states import Reg
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.types import CallbackQuery
from states import Admin

user = Router()
user_applications = {}

@user.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Вас приветствует Hive Flood\n\n"
        "Это система подачи заявок на вступление.\n"
        "Если хотите стать частью проекта — отправьте заявку, нажав кнопку ниже.\n\n"
        "После подачи администрация рассмотрит вашу анкету и свяжется с вами при одобрении.\n\n"
        "⬇️ Нажмите кнопку, чтобы начать"
        , reply_markup=kb.menu
    )

@user.message(F.text == "отправить заявку")
async def send_application(message: Message, state: FSMContext):
     user_id = message.from_user.id

     if user_id in user_applications and user_applications[user_id] == "pending":
        await message.answer("⏳ Ваша предыдущая заявка ещё рассматривается. Подождите ответа администрации.")
        return
     await message.answer(
        "📝 Форма заявки\n\n"
        "Пример:\n"
        "1. @username\n"
        "2. Желаемая ролб \n\n"
        "После этого заявка будет отправлена администрации.",
        reply_markup=ReplyKeyboardRemove()
    )
     await state.set_state(Reg.zaavka)


@user.message(Reg.zaavka)
async def receive_application(message: Message, state: FSMContext):
    application_text = message.text
    admin_id = 2141081959  
    user_id = message.from_user.id
    username = message.from_user.username or "без username"

    
    await message.answer(
        "✅ Ваша заявка отправлена!\nОжидайте решения администрации."
    )
    await state.clear()

   
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Одобрить",
                    callback_data=f"approve:{user_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Отклонить",
                    callback_data=f"reject:{user_id}"
                )
            ]
        ]
    )

    await message.bot.send_message(
        chat_id=admin_id,
        text=(
            "📨 Новая заявка\n\n"
            f"👤 Пользователь: @{username}\n"
            f"🆔 ID: {user_id}\n\n"
            "📄 Текст заявки:\n"
            f"{application_text}"
        ),
        reply_markup=keyboard

    )
    user_applications[user_id] = "pending"



@user.callback_query(lambda c: c.data and c.data.startswith("reject:"))
async def reject_application(callback: CallbackQuery):
    user_id = int(callback.data.split(":")[1])

    await callback.bot.send_message(
        chat_id=user_id,
        text="❌ Ваша заявка отклонена. Вы можете попробовать позже."
    )
    user_applications[user_id] = "rejected"

    await callback.answer("Пользователь уведомлён об отклонении", show_alert=True)

pending_links = {}

@user.callback_query(lambda c: c.data and c.data.startswith("approve:"))
async def approve_application(callback: CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    admin_id = callback.from_user.id

    
    pending_links[admin_id] = user_id

    await callback.message.answer(
        "✏️ Введите ссылку на чат, чтобы отправить пользователю:"
    )
    await callback.answer()  

@user.message()
async def send_link(message: Message):
    admin_id = message.from_user.id

    
    if admin_id not in pending_links:
        return  

    user_id = pending_links[admin_id]
    link = message.text

    await message.bot.send_message(
        chat_id=user_id,
        text=f"✅ Ваша заявка одобрена! Вот ссылка на чат:\n{link}"
    )
    user_applications[user_id] = "approved"

    await message.answer("Ссылка успешно отправлена пользователю!")

    
    del pending_links[admin_id]
