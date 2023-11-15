import logging
from aiogram import Router, F
from aiogram.filters import Command
from keyboards.keyboards import row_keyboard
from aiogram.types import Message

from config_reader import config

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    if (message.from_user.username is not None):
        await message.answer(
            text=f"Привет! Можешь зарегистрировать свой день рождения @{ message.from_user.username }, но сначала нужен пароль",
            reply_markup=row_keyboard(['/password'], 1)
        )
    else:
        await message.answer(
            text="Привет! У тебя не указан username в профиле, фу так(им/ой) быть\n"
                 "Возвращайся, когда исправишь",
            reply_markup=row_keyboard(['/start'], 1)
        )