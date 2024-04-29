from typing import Any

import aiogram
import aiogram.utils
import aiogram.utils.formatting
from aiogram.utils import formatting as fmt

from keyboards import keyboard
from bot import bot

class UserInfo:

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "UserInfo":
        return UserInfo(
            user_id=data.get("user_id", 0),
            tg_name=data.get("tg_name", ""),
            name=data.get("name", ""),
            phone=data.get("phone", ""),
            registration=data.get("registration", ""),
            need_shelter=data.get("need_shelter", False),
            family_size=data.get("family_size", ""),
            has_animal=data.get("has_animal", False),
            need_items=data.get("need_items", False),
            items=data.get("items", []),
            is_deliver=data.get("is_deliver", False),
            deliver_address=data.get("deliver_address", "")
        )
    def __init__(
            self,
            user_id: int, 
            name: str,
            tg_name: str,
            phone: str,
            registration: str,
            need_shelter: bool,
            family_size: str,
            has_animal: str,
            need_items: bool,
            items: list[str],
            is_deliver: bool,
            deliver_address: str
            ):
        self.user_id = user_id
        self.name = name
        self.tg_name = tg_name
        self.phone = phone
        self.registration = registration
        self.need_shelter = need_shelter
        self.family_size = family_size
        self.has_animal = has_animal
        self.need_items = need_items
        self.items = items
        self.is_deliver = is_deliver
        self.deliver_address = deliver_address
    
    async def send_to_chat(self, chat_id, send_keboard=False):
        text = str(self)
        if send_keboard:
            kwargs = {"reply_markup": keyboard.accept_reject}
        else:
            kwargs = {}
        await bot.bot.send_photo(
            chat_id=chat_id, 
            photo=self.registration, 
            caption=text,
            parse_mode=aiogram.enums.ParseMode.HTML,
            **kwargs
            )

    def _as_markdown(self):
        # link for user
        aiogram.utils.formatting.TextLink("Ссылка на пользователя", f"tg://user?id={self.user_id}")
        aiogram.utils.formatting.Text()

    def __str__(self) -> str:
        fields = []
        fields.append(f"Статус: Ожидает")
        fields.append(f"Телеграм: <a href=\"tg://user?id={self.user_id}\">{self.tg_name}</a>")
        fields.append(f"Имя: {self.name}")
        fields.append(f"Телефон: {self.phone}")
        fields.append(f"Нужно жильё: {'Да' if self.need_shelter else 'Нет'}")
        if self.need_shelter:
            fields.append("Размер семьи: " + self.family_size)
            fields.append("Есть животные: " + ("Да" if self.has_animal else "Нет"))
        fields.append(f"Необходимы вещи: {'Да' if self.need_items else 'Нет'}")
        if self.need_items:
            fields.append(f"Доставка: {'Да' if self.is_deliver else 'Самовывоз'}")
        if self.is_deliver:
            fields.append(f"Адрес доставки: {self.deliver_address}")
            fields.append(f"Вещи:\n\t* "+'\n\t* '.join(self.items))
        return "\n".join(fields)


_already_confirmed = set()

def already_confirm(user_id: int) -> bool:
    return user_id in _already_confirmed

def add_confirm(user_id: int):
    _already_confirmed.add(user_id)