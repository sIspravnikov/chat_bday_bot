from aiogram.fsm.state import StatesGroup, State

class RegisterBDay(StatesGroup):
    choosing_year = State()
    choosing_month = State()
    choosing_day = State()