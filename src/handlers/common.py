import aiogram
from aiogram import filters, types
from aiogram.fsm import context, state

router = aiogram.Router()


@router.message(filters.Command(commands=["start"]))
async def cmd_start(message: types.Message, state: context.FSMContext):
    await message.answer("Информация о боте, политика конфиденциальности и т.д.\n/help чтобы узнать больше")


@router.message(filters.Command(commands=["help"]))
async def cmd_help(message: types.Message, state: context.FSMContext):
    await message.answer("/form - заполнить форму")
