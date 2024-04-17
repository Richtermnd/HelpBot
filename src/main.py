import asyncio

from bot import bot
from handlers import common, form

async def main():
    print("start polling")
    bot.dp.include_routers(
        form.router,
        common.router,
    )
    await bot.dp.start_polling(bot.bot)


if __name__ == '__main__':
    asyncio.run(main())