
from aiogram import Router, F
from aiogram.filters import Command
from keyboards.keyboards import inline_button_builder, custom_keyboard
from aiogram.types import Message
from config_reader import config

router = Router()
secret_password = config.secret_password.get_secret_value()

@router.message(Command("start"))
async def start_cmd(message: Message):
    if (message.from_user.username is not None):
        await message.answer(
            f"Привет, @{message.from_user.username}! Для начала нужен пароль",
            reply_markup=inline_button_builder("Ввести пароль", "password")
        )
    elif (message.from_user.first_name is not None):
        await message.answer(
            f"Привет, {message.from_user.first_name}! У тебя не указан username в профиле\n"
            f"Возвращайся и снова жми /start, когда исправишь",
        )
    else:
        await message.answer(
            f"Что-то пошло не так",
        )


