import aiogram
from aiogram import filters, types, F
from aiogram.fsm import context, state
from aiogram.filters import callback_data

from keyboards import keyboard
from service import service
from custom_filters.custom_filters import ChatTypeFilter
from bot import bot
from handlers.enums import FormTexts


router = aiogram.Router()


@router.callback_query(keyboard.AcceptRejectCallback.filter(F.action == "accept"))
async def accept_reject(callback: types.CallbackQuery):
    text = callback.message.caption.split("\n")
    text[0] = f"Исполнитель: <a href=\"tg://user?id={callback.from_user.id}\">{callback.from_user.full_name}</a>"
    await callback.message.edit_caption(caption="\n".join(text), reply_markup=keyboard.complete, parse_mode=aiogram.enums.ParseMode.HTML)



@router.callback_query(keyboard.AcceptRejectCallback.filter(F.action == "reject"))
async def accept_reject(callback: types.CallbackQuery):
    text = callback.message.caption.split("\n")
    text[0] = f"Статус: Отклонено"
    await callback.message.edit_caption(caption="\n".join(text), parse_mode=aiogram.enums.ParseMode.HTML)


@router.callback_query(keyboard.CompleteCallback.filter())
async def complete(callback: types.CallbackQuery):
    text = callback.message.caption.split("\n")
    text[0] = f"Статус: Выполнено <a href=\"tg://user?id={callback.from_user.id}\">{callback.from_user.full_name}</a>"
    await callback.message.edit_caption(caption="\n".join(text), parse_mode=aiogram.enums.ParseMode.HTML)