import calendar
from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.keyboards import row_keyboard
from classes.RegisterBDay import RegisterBDay
from classes.Password import Password

router = Router()

available_years = [str(i) for i in range(int(datetime.now().year)-100, int(datetime.now().year))]
available_months = list(calendar.month_name[1:])
available_days = [str(i) for i in range(1, 32)]

def get_month_days(year: int, month: int):
    days = calendar.monthrange(int(year), list(calendar.month_name).index(month))[1]
    days_range = [str(i) for i in range(1, days+1)]
    return days_range

@router.message(Command("register"), StateFilter(Password.authenticated))
async def cmd_register(message: Message, state: FSMContext):
    print(available_years)
    await message.answer(
        text="Выбери год\n"
             "(Год не будет сохранен, нужен лишь для определения високосности года)",
        reply_markup=row_keyboard(available_years, 20)
    )
    await state.set_state(RegisterBDay.choosing_year)


@router.message(RegisterBDay.choosing_year, F.text.in_(available_years))
async def year_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_year=message.text.lower())
    await message.answer(
        text="Ок. Теперь выбери месяц:",
        reply_markup=row_keyboard(available_months, 4)
    )
    await state.set_state(RegisterBDay.choosing_month)

@router.message(StateFilter("RegisterBDay:choosing_year"))
async def year_chosen_incorrectly(message: Message):
    await message.answer(
        text="Сомневаюсь, что тебе столько лет :)\n"
             "Пожалуйста, выбери правильный год:",
        reply_markup=row_keyboard(available_years, 20)
    )

@router.message(RegisterBDay.choosing_month, F.text.in_(available_months))
async def month_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_month=message.text)
    user_data = await state.get_data()
    await message.answer(
        text="Записал. Теперь, день:",
        reply_markup=row_keyboard(get_month_days(user_data['chosen_year'], user_data['chosen_month']), 5)
    )
    await state.set_state(RegisterBDay.choosing_day)

@router.message(StateFilter("RegisterBDay:choosing_month"))
async def month_chosen_incorrectly(message: Message):
    await message.answer(
        text="Нет такого месяца\n"
             "Как дела на другой планете?",
        reply_markup=row_keyboard(available_months, 4)
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
async def day_chosen_incorrectly(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text="Некорректно введен день",
        reply_markup=row_keyboard(get_month_days(user_data['chosen_year'], user_data['chosen_month']), 5)
    )