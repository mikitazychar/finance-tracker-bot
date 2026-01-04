from aiogram.fsm.state import State, StatesGroup


class FinanceStates(StatesGroup):
    waiting_for_income = State()         # Ожидание ввода дохода
    waiting_for_category = State()       # Ожидание названия категории
    waiting_for_amount = State()         # Ожидание суммы расхода
