from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, \
    InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, \
    KeyboardButton, CallbackQuery





start_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text="Начать тестирование",callback_data='choose_test')]])

none_keyboard = InlineKeyboardMarkup(inline_keyboard=[])


async def choose_test_inline_keyboard(count: int)->InlineKeyboardMarkup:
    inline_keyboard = []
    for i in range(1, count+1):
        inline_keyboard.append(InlineKeyboardButton(text=str(i), callback_data=str(i)))
    return InlineKeyboardMarkup(inline_keyboard=[inline_keyboard])

