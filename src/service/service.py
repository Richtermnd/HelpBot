from typing import Any

import aiogram
import aiohttp

from bot import bot

class UserInfo:

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "UserInfo":
        return UserInfo(
            name=data.get("name", ""),
            phone=data.get("phone", ""),
            registration=data.get("registration", ""),
            need_shelter=data.get("need_shelter", False),
            need_items=data.get("need_items", False),
            items=data.get("items", []),
            is_deliver=data.get("is_deliver", False),
            deliver_address=data.get("deliver_address", "")
        )
    def __init__(
            self, 
            name: str,
            phone: str,
            registration: str,
            need_shelter: bool,
            need_items: bool,
            items: list[str],
            is_deliver: bool,
            deliver_address: str
            ):
        self.name = name
        self.phone = phone
        self.registration = registration
        self.need_shelter = need_shelter
        self.need_items = need_items
        self.items = items
        self.is_deliver = is_deliver
        self.deliver_address = deliver_address
    
    async def send_to_chat(self, chat_id):
        await bot.bot.send_photo(chat_id=chat_id, photo=self.registration, caption=str(self))
    
    # def dict(self) -> dict[str, Any]:
    #     return {
    #         "name": self.name,
    #         "phone": self.phone,
    #         "registration": self.registration,
    #         "need_shelter": self.need_shelter,
    #         "need_items": self.need_items,
    #         "items": self.items,
    #         "is_deliver": self.is_deliver,
    #         "deliver_address": self.deliver_address
    #     }
    def __str__(self) -> str:
        fields = []
        fields.append(f"Имя: {self.name}")
        fields.append(f"Телефон: {self.phone}")
        fields.append(f"Нужно жильё: {'Да' if self.need_shelter else 'Нет'}")
        fields.append(f"Нужны предметы: {'Да' if self.need_items else 'Нет'}")
        if self.need_items:
            fields.append(f"Доставка: {'Да' if self.is_deliver else 'Самовывоз'}")
        if self.is_deliver:
            fields.append(f"Адрес доставки: {self.deliver_address}")
            fields.append(f"Предметы:\n\t * "+'\n\t * '.join(self.items))
        return "\n".join(fields)
