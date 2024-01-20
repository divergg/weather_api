from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    new = State()
    old = State()