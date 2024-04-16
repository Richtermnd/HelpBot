from aiogram import types

def make_keyboard(items: list[str]) -> types.ReplyKeyboardMarkup:
    kb = [[types.KeyboardButton(text=item) for item in row] for row in items]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

