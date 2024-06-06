from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import text
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, PreCheckoutQuery, FSInputFile, LabeledPrice, \
    ShippingQuery
from aiogram.filters import Command, CommandStart
from sqlalchemy import select

from config import CHAT_ID, PAYMENT_TOKEN
from database import async_session
from keyboards import main_keyboard, categories_keyboard, subcategories_keyboard, products_keyboard, product_keyboard, \
    cart_keyboard, faq_keyboard, to_main
from models import Product
from utils import set_or_create_basket, get_cart, get_product, del_product
from utils import set_user

router = Router()


class HandlerState(StatesGroup):
    product: int = 0
    waiting_quantity = State()
    payment = State()
    tg_id: int = 0
    total_cost = 0


@router.message(CommandStart())
@router.callback_query(F.data == 'to_main')
async def cmd_start(message: Message | CallbackQuery):
    if isinstance(message, Message):
        await set_user(message.from_user.id)

        HandlerState.tg_id = message.from_user.id
        await message.answer("Welcome to bot!", reply_markup=main_keyboard())
    if isinstance(message, CallbackQuery):
        await message.message.answer("Main menu!", reply_markup=main_keyboard())


@router.callback_query(F.data.startswith("bot_"))
async def callbacks_main(callback: CallbackQuery):
    action = callback.data.split("_")[1]

    if action == "categories":
        await callback.message.answer("Choose category", reply_markup=await categories_keyboard())
    elif action == "cart":
        cart = await get_cart(HandlerState.tg_id)

        total_cost = 0
        message_string = ''
        for obj in cart:
            product = await get_product(obj.product_id)
            total_summ_for_product = obj.quantity * product.price
            total_cost += total_summ_for_product
            message_string += (f"*{product.title}*\n"
                               f"quantity in cart: {obj.quantity}\n"
                               f"price: {obj.quantity * product.price}\n")
        if total_cost > 0:
            HandlerState.total_cost = total_cost
            await callback.message.answer(
                message_string,
                parse_mode="Markdown"
            )
            await callback.message.answer(
                f"*Total cost: {total_cost}*",
                reply_markup=await cart_keyboard(),
                parse_mode="Markdown",
            )
        else:
            await callback.message.answer('Cart is empty\n Lets start shopping!', reply_markup=main_keyboard())

    elif action == "faq":
        await callback.message.answer('FAQ', reply_markup=faq_keyboard())

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
async def callbacks_product(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    HandlerState.product = int(action)
    await state.set_state(HandlerState.waiting_quantity)
    await callback.message.answer('Send quantity:')


@router.message(HandlerState.waiting_quantity)
async def waiting_quantity(message: Message, state: FSMContext):
    try:
        quantity = int(message.text)
        if quantity <= 0:
            raise ValueError
        user = message.from_user.id
        product = HandlerState.product

        await set_or_create_basket(tg_id=user, product_id=product, quantity=quantity)
        await message.answer('Product added to cart', reply_markup=main_keyboard())
        await state.clear()
    except ValueError:
        print('ValueError')
        await message.answer('Try again! Send an integer greater than zero')


# @router.message(HandlerState.waiting_quantity)
# async def waiting_quantity(message: Message, state: FSMContext):
#     print('HERE')
#     print('HERE')
#     print('HERE')
#     print('HERE')
#
#     try:
#         quantity = int(message.text)
#         if quantity <= 0:
#             raise ValueError
#         user = message.from_user.id
#         product = HandlerState.product
#
#         await set_or_create_basket(tg_id=user, product_id=product, quantity=quantity)
#         await message.answer('Product added to cart', reply_markup=main_keyboard())
#         await state.clear()
#     except ValueError:
#         print('ValueError')
#         await message.answer('Try again! Send an integer greater than zero')


@router.callback_query(F.data == 'delete_products')
async def callbacks_delete_product(callback: CallbackQuery):
    cart = await get_cart(HandlerState.tg_id)
    keyboard = InlineKeyboardBuilder()
    for obj in cart:
        prod = await get_product(obj.product_id)

        keyboard.add(
            InlineKeyboardButton(
                text=f"{prod.title}",
                callback_data=f"del_product_{prod.id}")
        )
    keyboard.add(to_main)

    await callback.message.answer(
        'Choose product to delete',
        reply_markup=keyboard.adjust(2).as_markup(),
    )


@router.callback_query(F.data.startswith("del_product_"))
async def callbacks_del_product(callback: CallbackQuery, ):
    action = callback.data.split("_")[2]
    await del_product(tg_id=HandlerState.tg_id, product_id=int(action))
    await callback.message.answer("Product removed from cart!", reply_markup=main_keyboard())

# @router.callback_query(F.data==)
# async def callbacks_products(callback: CallbackQuery,): checkout
