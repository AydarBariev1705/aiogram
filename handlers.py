from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.markdown import text
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.filters import Command, CommandStart
from sqlalchemy import select

from config import CHAT_ID
from database import async_session
from keyboards import main_keyboard, categories_keyboard, subcategories_keyboard, products_keyboard, product_keyboard
from models import Product

router = Router()

FAQ = 'FAQ'


class HandlerState(StatesGroup):
    product = 0
    waiting_quantity = State()


@router.message(CommandStart())
@router.callback_query(F.data == 'to_main')
async def cmd_start(message: Message | CallbackQuery):
    if isinstance(message, Message):
        # await set_user(message.from_user.id)

        await message.answer("Hello!", reply_markup=main_keyboard())


@router.callback_query(F.data.startswith("bot_"))
async def callbacks_main(callback: CallbackQuery):
    action = callback.data.split("_")[1]

    if action == "categories":
        await callback.message.answer("Choose category", reply_markup=await categories_keyboard())

    elif action == "cart":

        await callback.message.answer(f"cart")
    elif action == "faq":
        await callback.message.answer(FAQ)

    await callback.answer()


@router.callback_query(F.data.startswith("category_"))
async def callbacks_subcat(callback: CallbackQuery):
    action = callback.data.split("_")[1]
    await callback.message.answer("Choose subcategory", reply_markup=await subcategories_keyboard(int(action)))


@router.callback_query(F.data.startswith("subcategory_"))
async def callbacks_products(callback: CallbackQuery):
    action = callback.data.split("_")[1]
    await callback.message.answer("Choose product", reply_markup=await products_keyboard(int(action)))


@router.callback_query(F.data.startswith("products_"))
async def callbacks_products(callback: CallbackQuery):
    action = callback.data.split("_")[1]
    keyboard, product = await product_keyboard(int(action))
    await callback.message.answer_photo(
        photo=FSInputFile(
            path=f'aiogramBariev/{product.image}',

        ),
        caption=f"{product.description}\n\nprice: {product.price}",
        reply_markup=keyboard,
    )


@router.callback_query(F.data.startswith("product_"))
async def callbacks_products(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    HandlerState.product = int(action)
    await state.set_state(HandlerState.waiting_quantity)
    await callback.message.answer('Send quantity:')


@router.message(HandlerState.waiting_quantity)
async def newsletter_message(message: Message, state: FSMContext):
    user = message.from_user.id
    product = HandlerState.product
    quantity = int(message.text)
    print('user', user,)
    print('product', product, )
    print('quantity', quantity)
    await message.answer('Added to cart', reply_markup=main_keyboard())

    await state.clear()

# @router.callback_query(F.data.startswith("subcategory_"))
# async def callbacks_products(callback: CallbackQuery):
#     action = callback.data.split("_")[1]
#     async with async_session() as session:
#         products = await session.scalars(select(Product).where(Product.subcategory_id == int(action)))
#     for product in products:
#         buttons = [
#             [
#                 InlineKeyboardButton(text=f"Add to basket", callback_data=f"to_basket"),
#                 InlineKeyboardButton(text=f"To main menu", callback_data=f"to_main"),
#             ],
#         ]
#         keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
#         await callback.message.answer_photo(
#             photo=FSInputFile(path=f'aiogramBariev/{product.image}'),
#         )
#         await callback.message.answer(
#             f"{product.description}\n\nprice: {product.price}",
#             reply_markup=keyboard,
#         )
