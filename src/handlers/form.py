import re

import aiogram
from aiogram import filters, types
from aiogram.fsm import context, state

from keyboards import keyboard
from service import service
from custom_filters.custom_filters import ChatTypeFilter
from bot import bot


router = aiogram.Router()
router.message.filter(ChatTypeFilter("private"))

class FormState(state.StatesGroup):
    name_state = state.State()
    phone_state = state.State()
    registration_state = state.State()
    
    need_shelter_state = state.State()
    family_size_state = state.State()
    has_animals_state = state.State()
    prefer_district_state = state.State()

    need_items_state = state.State()
    items_state = state.State()
    is_deliver_state = state.State()
    deliver_address_state = state.State()
    confirm_state = state.State()
    cancel_state = state.State()


state_map = {
    # Required
    FormState.name_state: {
        "text": "Ваше ФИО:",
        "reply_markup": keyboard.make_keyboard([["Отмена"]])
    },
    FormState.phone_state: {
        "text": "Ваш контактный номер телефона:",
        "reply_markup": keyboard.make_keyboard([["Отмена"]])
    },
    FormState.registration_state: {
        "text": "Пришлите фото вашей прописки:",
        "reply_markup": keyboard.make_keyboard([["Отмена"]])
    },

    # Shelter stuff
    FormState.need_shelter_state: {
        "text": "Нужно ли вам жильё?",
        "reply_markup": keyboard.make_keyboard([["Да", "Нет"], ["Отмена"]])
    },
    FormState.family_size_state: {
        "text": "Сколько человек в семье?",
        "reply_markup": keyboard.make_keyboard([["Отмена"]])
    },
    FormState.has_animals_state: {
        "text": "Есть ли у вас животные?",
        "reply_markup": keyboard.make_keyboard([["Да", "Нет"], ["Отмена"]])
    },
    FormState.prefer_district_state: {
        "text": "Предпочитаемый район?",
        "reply_markup": keyboard.make_keyboard([["Отмена"]])
    },

    # Items
    FormState.need_items_state: {
        "text": "Нужны ли вам вещи?",
        "reply_markup": keyboard.make_keyboard([["Да", "Нет"], ["Отмена"]])
    },

    # Select deliver or pickup
    FormState.is_deliver_state: {
        "text": "Доставка или самовывоз?",
        "reply_markup": keyboard.make_keyboard([["Доставка", "Самовывоз"], ["Отмена"]])
    },

    # Is deliver 
    FormState.items_state: {
        "text": "Укажите необходимые вещи через запятую:",
        "reply_markup": keyboard.make_keyboard([["Отмена"]])
    },
    FormState.deliver_address_state: {
        "text": "Укажите адрес доставки:",
        "reply_markup": keyboard.make_keyboard([["Отмена"]])
    },
    FormState.confirm_state: {
        "text": "Нажимая подтвердить вы даёте согласие на обработку персональных данных.",
        "reply_markup": keyboard.make_keyboard([["Подтвердить", "Заполнить заново"], ["Я отказываюсь"]])
    }
}


async def goto(state: FormState, context: context.FSMContext, message: types.Message):
    msg = state_map[state]    
    await message.answer(**msg)
    await context.set_state(state)

async def goto_confirm(context: context.FSMContext, message: types.Message):
    user = service.UserInfo.from_dict(await context.get_data())
    await user.send_to_chat(message.chat.id)
    await goto(FormState.confirm_state, context, message)
    await context.set_state(FormState.confirm_state)

@router.message(filters.StateFilter(None), filters.Command(commands=["form"]))
async def cmd_form(message: types.Message, state: context.FSMContext):
    await message.answer("Сейчас вам предстоит заполнить анкету.\n <ссылка на документ о согласии на обработку перосональных данных>")
    await goto(FormState.name_state, state, message)


@router.message(FormState.name_state)
async def form_name(message: types.Message, state: context.FSMContext):
    if message.text == "Отмена":
        await cancel(message, state)
        return
    await state.update_data(name=message.text)
    await goto(FormState.phone_state, state, message)


@router.message(FormState.phone_state)
async def form_phone(message: types.Message, state: context.FSMContext):
    if message.text == "Отмена":
        await cancel(message, state)
        return
    if not re.match(r"\(?\+[0-9]{1,3}\)? ?-?[0-9]{1,3} ?-?[0-9]{3,5} ?-?[0-9]{4}( ?-?[0-9]{3})?", message.text):
        await message.answer("Некорректный номер телефона.")
        await goto(FormState.phone_state, state, message)
        return
    await state.update_data(phone=message.text)
    await goto(FormState.registration_state, state, message)

@router.message(FormState.registration_state)
async def form_registration(message: types.Message, state: context.FSMContext):
    if message.text == "Отмена":
        await cancel(message, state)
        return
    
    if not message.photo:
        await message.answer("Пожалуйста, прикрепите фото.")
        await goto(FormState.registration_state, state, message)
        return
    
    # Get photo from message
    photo = message.photo[-1]
    # save photo id to context
    await state.update_data(registration=photo.file_id)
    # Go to next context
    await goto(FormState.need_shelter_state, state, message)

# --- Shelter dialog ---
@router.message(FormState.need_shelter_state, aiogram.F.text.in_(("Да", "Нет", "Отмена")))
async def form_need_shelter(message: types.Message, state: context.FSMContext):
    if message.text == "Отмена":
        await cancel(message, state)
        return
    
    if message.text == "Нет":
        await state.update_data(need_shelter=False)
        await goto(FormState.need_items_state, state, message)
    else:
        await state.update_data(need_shelter=True)
        await goto(FormState.family_size_state, state, message)
    

@router.message(FormState.family_size_state)
async def form_family_size(message: types.Message, state: context.FSMContext):
    if message.text == "Отмена":
        await cancel(message, state)
        return
    await state.update_data(family_size=message.text)
    await goto(FormState.has_animals_state, state, message)


@router.message(FormState.has_animals_state, aiogram.F.text.in_(("Да", "Нет", "Отмена")))
async def form_has_animals(message: types.Message, state: context.FSMContext):
    if message.text == "Отмена":
        await cancel(message, state)
        return
    await state.update_data(has_animals=message.text)
    await goto(FormState.need_items_state, state, message)


# --- Items dialog ---

@router.message(FormState.need_items_state, aiogram.F.text.in_(("Да", "Нет", "Отмена")))
async def form_need_items(message: types.Message, state: context.FSMContext):
    if message.text == "Отмена":
        await cancel(message, state)
        return
    if message.text == "Нет":
        await state.update_data(need_items=False)
        await goto_confirm(state, message)
        return
    await state.update_data(need_items=True)
    await goto(FormState.is_deliver_state, state, message)


@router.message(FormState.is_deliver_state, aiogram.F.text.in_(("Доставка", "Самовывоз", "Отмена")))
async def form_is_deliver(message: types.Message, state: context.FSMContext):
    if message.text == "Отмена":
        await cancel(message, state)
        return
    if message.text == "Самовывоз":
        await state.update_data(is_deliver=False)
        await message.answer("""
Пункты выдачи:
Оренбург - ул. новая 4, время работы с 10:00 до 20:00
Оренбургский район - ул. степана разина 209, время работы с 9:00 до 18:00""")
        await goto_confirm(state, message)
        return
    
    await state.update_data(is_deliver=True)
    await goto(FormState.items_state, state, message)


@router.message(FormState.items_state)
async def form_items(message: types.Message, state: context.FSMContext):
    if message.text == "Отмена":
        await cancel(message, state)
        return
    items = [item.strip() for item in message.text.split(",")]
    await state.update_data(items=items)
    await goto(FormState.deliver_address_state, state, message)


@router.message(FormState.deliver_address_state)
async def form_deliver_address(message: types.Message, state: context.FSMContext):
    if message.text == "Отмена":
        await cancel(message, state)
        return
    await state.update_data(deliver_address=message.text)
    await goto_confirm(state, message)


@router.message(FormState.confirm_state, aiogram.F.text.in_(("Подтвердить", "Заполнить заново", "Я отказываюсь")))
async def form_confirm(message: types.Message, state: context.FSMContext):
    if message.text == "Я отказываюсь":
        await message.answer("Данные удалены.\nВы всегда можете заполнить анкету снова.", reply_markup=types.ReplyKeyboardRemove())
        await cancel(message, state)
        return
    if message.text == "Подтвердить":
        await message.answer(
            text="Данные подтверждены.",
            reply_markup=types.ReplyKeyboardRemove()
            )
        user = service.UserInfo.from_dict(await state.get_data())
        await user.send_to_chat(bot.chat_id)
        await state.clear()
        return
    await state.set_data({})
    await goto(FormState.name_state, state, message)


async def cancel(message: types.Message, context: context.FSMContext):
    await context.set_state(None)
    await context.clear()
    await message.answer("Данные удалены.", reply_markup=types.ReplyKeyboardRemove())