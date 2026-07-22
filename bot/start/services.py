from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandObject
from aiogram.utils.deep_linking import create_start_link, decode_payload
from aiogram.enums import ChatAction

from ..core.request import get_all_test, create_session, create_user, join_session

from .keyboard import (start_inline_keyboard, none_keyboard,
                       choose_test_inline_keyboard, creat_butten_links)

from .fms import Registration


class Services:
    async def _save_state(self,message_text, state: FSMContext,data:dict):
        data = await state.get_data()
        answers = data.get("answers")
        answers.update({data.get('i'): message_text})
        await state.update_data(answers=answers, i=str(int(data.get('i')) + 1))

        return answers

    async def start(self,message: Message) -> None:
        create_user(message.from_user.id)
        await message.answer("Выбор:", reply_markup=start_inline_keyboard)

    async def start_deep_link(self,message: Message,command: CommandObject,state: FSMContext) -> None:
        tests = get_all_test()
        session_id, test_id, user_id = decode_payload(command.args).split("_")
        await state.update_data(tests=tests.get(test_id),i=1, answers={},session_id=session_id,
                                user_id=user_id)
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
        tests = data.get("tests")

        await state.set_state(Registration.answer_to_questions)
        await state.update_data(tests=tests.get(call.data), i=1, answers={})

        await call.message.edit_text(f"Вы выбрали: {tests.get(call.data).get('name')}",
                                     reply_markup=none_keyboard)
        await call.message.answer(tests.get(call.data).get("questions").get("1"))


    async def answer_to_questions(self,message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        questions = data.get("tests").get("questions")
        index_questions = str(int(data.get('i')) + 1)
        answers = await self._save_state(message_text=message.text,state=state,data=data)

        if questions.get(index_questions) == None:
            test_id = data.get("tests").get("id")

            session_id = create_session(answers=answers,
                                 tid=message.from_user.id,test_id=test_id)

            link = await create_start_link(message.bot,
                                 payload=f"{session_id}_{test_id}_{message.from_user.id}", encode=True)
            await message.answer(f"Отлично, Вы прошли тест"
                                 f"\nСкопируйте и пришлите эту ссылку другу, чтобы он смог пройти тест",
                                 reply_markup= await creat_butten_links(url=link))
            await state.clear()
            return

        await message.answer(questions.get(index_questions))



    async def answer_to_questions_friend(self, message: Message, state: FSMContext) -> None:
        data = await state.get_data()

        questions = data.get("tests").get("questions")
        index_questions = str(int(data.get('i')) + 1)
        answers = await self._save_state(message_text=message.text, state=state, data=data)

        if questions.get(str(int(data.get('i')) + 1)) == None:
            message_edit = await message.answer("Ваши ответы обрабатываются, подождите")
            await message.bot.send_chat_action(message.chat.id,ChatAction.TYPING)

            result = join_session(answers=answers,
                                            tid=message.from_user.id, session_id=data.get("session_id"))

            await message_edit.edit_text(f"Результат теста: {result}")
            await message.bot.send_message(chat_id=data.get("user_id"),
                                           text=f"Результат теста с пользователем"
                                                f" {message.from_user.first_name}\n"
                                                + result)
            await state.clear()
            return


        await message.answer(questions.get(index_questions))