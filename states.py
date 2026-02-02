from aiogram.fsm.state import StatesGroup, State

class Reg(StatesGroup):
    zaavka = State()

class Admin(StatesGroup):
    waiting_link = State()
