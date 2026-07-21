from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandObject
from aiogram.utils.deep_linking import create_start_link, decode_payload
from ..core.request import get_all_test, create_session, create_user, join_session

from .keyboard import start_inline_keyboard, none_keyboard, choose_test_inline_keyboard

from .fms import Registration



class Services:
    async def start(self,message: Message) -> None:
        create_user(message.from_user.id)
        await message.answer("Выбор:", reply_markup=start_inline_keyboard)

    async def start_deep_link(self,message: Message,command: CommandObject,state: FSMContext) -> None:
        tests = get_all_test()
        session_id, test_id = decode_payload(command.args).split("_")
        await state.update_data(tests=tests.get(test_id),i=1, answers={},session_id=session_id)
        await state.set_state(Registration.answer_to_questions1)
        await message.answer(f"Тест: {tests.get(test_id).get('name')}")
        await message.answer(f"Вопрос: {tests.get(test_id).get('questions').get('1')}")


    async def choose_test(self,call:CallbackQuery, state: FSMContext) -> None:
        tests = get_all_test()
        await state.update_data(tests=tests)
        await state.set_state(Registration.choose_test)
        text = ""
        for i in range(1, len(tests) + 1):
            text += f"{i}: " + tests.get(str(i)).get("name") + "\n"

        await call.message.edit_text(text,
                        reply_markup=await choose_test_inline_keyboard(len(tests)))

    async def set_test(self,call: CallbackQuery, state: FSMContext) -> None:
        data = await state.get_data()
        data = data.get("tests")
        await state.set_state(Registration.answer_to_questions)
        await state.update_data(tests=data.get(call.data),i=1, answers={})
        await call.message.edit_text(f"Вы выбрали: {data.get(call.data).get('name')}",
                                     reply_markup=none_keyboard)
        await call.message.answer(data.get(call.data).get("questions").get("1"))

    async def answer_to_questions(self,message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        questions = data.get("tests").get("questions")

        answers = data.get("answers")
        answers.update({data.get('i'): message.text})

        if questions.get(str(int(data.get('i')) + 1)) == None:
            session_id = create_session(answers=answers,
                                 tid=message.from_user.id,test_id=data.get("tests").get("id"))
            test_id = data.get("tests").get("id")
            link = await create_start_link(message.bot, payload=f"{session_id}_{test_id}", encode=True)
            await message.answer(f"Отлично, вы прошли тест\n Вот ссылка для {link}")
            await state.clear()
            return


        await state.update_data(answers=answers,i=str(int(data.get('i')) + 1))

        await message.answer(data.get("tests").get("questions").\
                             get(str(int(data.get('i')) + 1)))

    async def answer_to_questions1(self, message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        questions = data.get("tests").get("questions")

        answers = data.get("answers")
        answers.update({data.get('i'): message.text})

        if questions.get(str(int(data.get('i')) + 1)) == None:
            result = join_session(answers=answers,
                                        tid=message.from_user.id, session_id=data.get("session_id"))

            await message.answer(f"Результат теста: {result}")
            await state.clear()
            return

        await state.update_data(answers=answers, i=str(int(data.get('i')) + 1))

        await message.answer(data.get("tests").get("questions"). \
                             get(str(int(data.get('i')) + 1)))
