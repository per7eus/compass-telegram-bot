from aiogram.fsm.state import StatesGroup, State

class Registration(StatesGroup):
    choose_test = State()
    answer_to_questions = State()
    answer_to_questions1 = State()