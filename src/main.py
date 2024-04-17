import asyncio

from bot import bot
from handlers import common, form

async def main():
    bot.dp.message.filter()
    bot.dp.include_routers(
        form.router,
        common.router,
    )
    print("start polling")
    await bot.dp.start_polling(bot.bot)


if __name__ == '__main__':
    asyncio.run(main())