from aiogram.fsm.state import StatesGroup, State

class Password(StatesGroup):
    wait_for_pass = State()
    authenticated = State()