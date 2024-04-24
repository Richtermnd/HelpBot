import aiogram
from aiogram import filters, types
from aiogram.fsm import context, state

from keyboards import keyboard
from handlers import enums

router = aiogram.Router()


@router.message(filters.Command(commands=["start"]))
async def cmd_start(message: types.Message, state: context.FSMContext):
    await message.answer(
        enums.FormTexts.start_message,
        reply_markup=keyboard.make_keyboard([["Заполнить форму"]]))