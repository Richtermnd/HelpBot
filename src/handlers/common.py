import aiogram
from aiogram import filters, types
from aiogram.fsm import context, state

from keyboards import keyboard

router = aiogram.Router()


@router.message(filters.Command(commands=["start"]))
async def cmd_start(message: types.Message, state: context.FSMContext):
    # await message.answer("Информация о боте, политика конфиденциальности и т.д.\n/help чтобы узнать больше")
    await message.answer(
        "Этот бот создан для сбора информации о пострадавших в Оренбурге во время затопления.",
        reply_markup=keyboard.make_keyboard([["Заполнить форму"]]))