from aiogram import Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, FSInputFile
from aiogram.filters import CommandStart
from config import FAQ
from keyboards import main_keyboard, categories_keyboard, subcategories_keyboard, products_keyboard, product_keyboard, \
    cart_keyboard, faq_keyboard, to_main, faq_answer_keyboard
from utils import set_or_create_basket, get_cart, get_product, del_product, set_user, set_total_cost

router = Router()


@router.message(CommandStart())
@router.callback_query(F.data == 'to_main')
async def cmd_start(message: Message | CallbackQuery):
    if isinstance(message, Message):
        await set_user(message.from_user.id)

        await message.answer(
            "Welcome to bot!",
            reply_markup=main_keyboard(),
        )
    if isinstance(message, CallbackQuery):
        await message.message.answer(
            "Main menu!",
            reply_markup=main_keyboard(),
        )


@router.callback_query(F.data.startswith("bot_"))
async def callbacks_main(callback: CallbackQuery):
    action = callback.data.split("_")[1]

    if action == "categories":
        await callback.message.answer(
            "Choose category",
            reply_markup=await categories_keyboard(),
        )
    elif action == "cart":
        cart = await get_cart(callback.from_user.id)
        total_cost, message_string = await set_total_cost(cart)

        if total_cost > 0:
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
            await callback.message.answer(
                'Cart is empty\n Lets start shopping!',
                reply_markup=main_keyboard(),
            )

    elif action == "faq":
        await callback.message.answer(
            'FAQ',
            reply_markup=faq_keyboard(),
        )

    await callback.answer()


@router.callback_query(F.data.startswith("category_"))
async def callbacks_subcat(callback: CallbackQuery):
    action = callback.data.split("_")[1]
    await callback.message.answer(
        "Choose subcategory",
        reply_markup=await subcategories_keyboard(int(action)),
    )


@router.callback_query(F.data.startswith("faq_"))
async def callbacks_faq(callback: CallbackQuery):
    action = callback.data.split("_")[1]
    await callback.message.answer(
        FAQ[int(action)][1]
        , reply_markup=faq_answer_keyboard(),
    )


@router.callback_query(F.data.startswith("subcategory_"))
async def callbacks_products(callback: CallbackQuery):
    action = callback.data.split("_")[1]
    await callback.message.answer(
        "Choose product",
        reply_markup=await products_keyboard(int(action)),
    )


@router.callback_query(F.data.startswith("products_"))
async def callbacks_products(callback: CallbackQuery):
    action = callback.data.split("_")[1]
    keyboard, product, count = await product_keyboard(int(action))
    await callback.message.answer_photo(
        photo=product.image,
        caption=f"{product.description}\n\nprice: {product.price}",
        reply_markup=keyboard,
    )


@router.callback_query(F.data.startswith("btn_"))
async def callbacks_plus(callback: CallbackQuery):
    action = callback.data.split("_")
    count = int(action[2])
    prod_id = int(action[3])

    if action[1] == 'plus':
        keyboard, product, count = await product_keyboard(
            prod_id=prod_id,
            count=count + 1,
        )
        await callback.message.answer_photo(
            photo=product.image,
            caption=f"{product.description}\n\nprice: {product.price}",
            reply_markup=keyboard,
        )

    elif action[1] == 'minus':
        keyboard, product, count = await product_keyboard(
            prod_id=prod_id,
            count=count - 1,
        )
        await callback.message.answer_photo(
            photo=product.image,
            caption=f"{product.description}\n\nprice: {product.price}",
            reply_markup=keyboard,
        )


@router.callback_query(F.data.startswith("accept_"))
async def callbacks_plus(callback: CallbackQuery):
    action = callback.data.split("_")
    count = int(action[1])
    prod_id = int(action[2])
    tg_id = callback.from_user.id
    await set_or_create_basket(
        tg_id=tg_id,
        product_id=prod_id,
        quantity=count,
    )
    await callback.message.answer(
        'Product added to cart',
        reply_markup=main_keyboard(),
    )


@router.callback_query(F.data == 'delete_products')
async def callbacks_delete_product(callback: CallbackQuery):
    cart = await get_cart(callback.from_user.id)
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
    await del_product(
        tg_id=callback.from_user.id,
        product_id=int(action),
    )
    await callback.message.answer(
        "Product removed from cart!",
        reply_markup=main_keyboard(),
    )
