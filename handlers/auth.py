from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, ReplyKeyboardRemove
from config_reader import config

from keyboards.keyboards import row_keyboard
from classes.Password import Password


router = Router()

secret_password = config.secret_password.get_secret_value()

@router.message(Command("password"))
async def password(message: Message, state: FSMContext):
    await message.answer(
        text=f"Введи пароль:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Password.wait_for_pass)

@router.message(Password.wait_for_pass, F.text == secret_password)
async def password(message: Message, state: FSMContext):
    await message.answer(
        text=f"Ага, жми кнопку регистрации",
        reply_markup=row_keyboard(['/register'], 1)
    )
    await state.set_state(Password.authenticated)

@router.message(StateFilter("Password:wait_for_pass"))
async def wrong_password(message: Message, state: FSMContext):
    await message.answer(
        text="Неа"
    )
