from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, CallbackQuery
from config_reader import config

from keyboards.keyboards import inline_button_builder
from classes.Password import Password


router = Router()

secret_password = config.secret_password.get_secret_value()

@router.callback_query(F.data == "password")
async def password_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введи пароль ниже:")
    await callback.answer()
    await state.set_state(Password.wait_for_pass)

@router.message(Password.wait_for_pass, F.text == secret_password)
async def password(message: Message, state: FSMContext):
    await message.answer(
        text=f"Верно, жми кнопку регистрации",
        reply_markup=inline_button_builder("Регистрация", "register")
    )
    await state.set_state(Password.authenticated)

@router.message(StateFilter("Password:wait_for_pass"))
async def wrong_password(message: Message, state: FSMContext):
    await message.answer(
        text="Не-а"
    )
    # тут надо будет добавить запись в БД количества попыток и блочить нахер при попытках брута