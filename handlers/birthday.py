import calendar
from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.keyboards import row_keyboard

router = Router()

available_years = [str(i) for i in range(int(datetime.now().year)-50, int(datetime.now().year))]
available_months = list(calendar.month_name[1:])
available_days = [str(i) for i in range(1, 32)]

class RegisterBDay(StatesGroup):
    choosing_year = State()
    choosing_month = State()
    choosing_day = State()

# обработчик регистрации, сразу спрашиваем год
@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    print(available_years)
    await message.answer(
        text="Выберите год:",
        reply_markup=row_keyboard(available_years, 10)
    )
    await state.set_state(RegisterBDay.choosing_year)


@router.message(RegisterBDay.choosing_year, F.text.in_(available_years))
async def year_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_year=message.text.lower())
    await message.answer(
        text="Записал. Теперь, месяц:",
        reply_markup=row_keyboard(available_months, 4)
    )
    await state.set_state(RegisterBDay.choosing_month)

@router.message(StateFilter("RegisterBDay:choosing_year"))
async def year_chosen_incorrectly(message: Message):
    await message.answer(
        text="Год недоступен\n"
             "Пожалуйста, родитесь позже(или раньше) :)",
        reply_markup=row_keyboard(available_years)
    )

@router.message(RegisterBDay.choosing_month, F.text.in_(available_months))
async def month_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_month=message.text.lower())
    await message.answer(
        text="Записал. Теперь, день:",
        reply_markup=row_keyboard(available_days, 10)
    )
    await state.set_state(RegisterBDay.choosing_day)

@router.message(StateFilter("RegisterBDay:choosing_month"))
async def month_chosen_incorrectly(message: Message):
    await message.answer(
        text="Нет такого месяца\n"
             "Вы с другой планеты?",
        reply_markup=row_keyboard(available_months)
    )

@router.message(RegisterBDay.choosing_day, F.text.in_(available_days))
async def day_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_day=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        text=f"Дата рождения {user_data['chosen_day']} {user_data['chosen_month']} {user_data['chosen_year']}\n"
             f"Всё верно?",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


@router.message(RegisterBDay.choosing_day)
async def day_chosen_incorrectly(message: Message):
    await message.answer(
        text="Таких дней не знаю",
        reply_markup=row_keyboard(available_days)
    )