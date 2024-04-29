from aiogram import types
from aiogram.filters import callback_data
from enums import TaskState

class AcceptRejectCallback(callback_data.CallbackData, prefix="accept_reject"):
    action: str

class CompleteCallback(callback_data.CallbackData, prefix="complete"):
    pass


def make_keyboard(items: list[str]) -> types.ReplyKeyboardMarkup:
    kb = [[types.KeyboardButton(text=item) for item in row] for row in items]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


accept_reject = types.InlineKeyboardMarkup(
    inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Принять", callback_data=AcceptRejectCallback(action="accept").pack()),
                types.InlineKeyboardButton(text="Отклонить", callback_data=AcceptRejectCallback(action="reject").pack()),
            ]
        ]
)


complete = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Завершено", callback_data=CompleteCallback().pack())
        ],
    ]
)