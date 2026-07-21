from aiogram import Router, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from .services import Services

from .fms import Registration

router = Router()

services = Services()


@router.message(CommandStart(deep_link=True))
async def start(message: Message, command: CommandObject, state: FSMContext):
    await services.start_deep_link(message, command, state)


@router.message(CommandStart())
async def start(message: Message):
    await services.start(message)



@router.callback_query(F.data == "choose_test")
async def choose_test(call: CallbackQuery, state: FSMContext):
    await services.choose_test(call, state)


@router.callback_query(Registration.choose_test)
async def set_test(call: CallbackQuery, state: FSMContext):
    await services.set_test(call, state)


@router.message(Registration.answer_to_questions, F.text)
async def answer_to_questions(message: Message, state: FSMContext):
    await services.answer_to_questions(message, state)

@router.message(Registration.answer_to_questions1, F.text)
async def answer_to_questions(message: Message, state: FSMContext):
    await services.answer_to_questions1(message, state)
