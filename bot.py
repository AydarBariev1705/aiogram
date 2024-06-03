from aiogram import Bot, types, Dispatcher
from aiogram.utils.markdown import text
from aiogram.filters.command import Command
from aiogram import F
import asyncio

from sqlalchemy import select

from models import Category
from config import TOKEN
from database import session

bot = Bot(token=TOKEN)
dp = Dispatcher()
FAQ = 'q1?\na1\nq2?\na2'


##
def main_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Categories", callback_data="bot_categories"),
            types.InlineKeyboardButton(text="Cart", callback_data="bot_cart")
        ],
        [types.InlineKeyboardButton(text="FAQ", callback_data="bot_faq")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_categories():
    categories = session.execute(select(Category.title, Category.id)).all()
    for category in categories:
        print(category[1])
    buttons = [
        [
            types.InlineKeyboardButton(text=f"{category[0]}", callback_data=f"category_{category[1]}")
        ] for category in categories
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


@dp.callback_query(F.data.startswith("bot_"))
async def callbacks_num(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]

    if action == "categories":
        buttons = session.execute(select(Category.title)).all()
        for button in buttons:
            print(button[0])

        await callback.message.answer("categories", reply_markup=get_categories())

    elif action == "cart":

        await callback.message.answer(f"cart")
    elif action == "faq":
        await callback.message.answer(FAQ)

    await callback.answer()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!", reply_markup=main_keyboard())


help_message = text(
    "HELP",

    sep="\n"
)


@dp.message(Command("help"))
async def cmd_start(message: types.Message):
    await message.answer(help_message)


async def main():
    print('Start')

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
