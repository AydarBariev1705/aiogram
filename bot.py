import asyncio
from config import TOKEN
from handlers import router
from payment_handler import order, process_pre_checkout_query, successful_payment
from aiogram import Bot, Dispatcher, F

from admin import admin


async def main():
    bot = Bot(token=TOKEN)

    dp = Dispatcher()
    dp.include_routers(router, admin)
    dp.callback_query.register(order, F.data == 'checkout')
    dp.pre_checkout_query.register(process_pre_checkout_query)
    dp.message.register(successful_payment, F.successful_payment)
    print('Start')

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
