from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, \
    InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, \
    KeyboardButton, CallbackQuery,\
    CopyTextButton





start_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text="Начать тестирование",callback_data='choose_test')]])

none_keyboard = InlineKeyboardMarkup(inline_keyboard=[])


async def choose_test_inline_keyboard(count: int)->InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text=str(i), callback_data=str(i),style="primary")
        for i in range(1, count + 1)
    ]

    inline_keyboard = [
        buttons[i:i + 3]
        for i in range(0, len(buttons), 3)
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def creat_butten_links(url):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text="Скопировать ссылку для друга", copy_text=CopyTextButton(text=url), style="success")]])