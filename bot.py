import asyncio

from aiogram.types import Message

from config import TOKEN
from handlers import router
from aiogram import Bot, Dispatcher
# from admin import admin


async def main():
    bot = Bot(token=TOKEN)

    dp = Dispatcher()
    dp.include_router(router)

    print('Start')
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
