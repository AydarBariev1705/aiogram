from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import FAQ
from utils import get_categories, get_subcategories, get_products, get_product


def main_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="Categories", callback_data="bot_categories"),
            InlineKeyboardButton(text="Cart", callback_data="bot_cart")
        ],
        [InlineKeyboardButton(text="FAQ", callback_data="bot_faq")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


to_main = InlineKeyboardButton(
    text='To main menu',
    callback_data='to_main')


async def categories_keyboard():
    categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in categories:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{category.title}",
                callback_data=f"category_{category.id}")
        )
        keyboard.add(to_main)

    return keyboard.adjust(2).as_markup()


def faq_keyboard():
    keyboard = InlineKeyboardBuilder()
    for number, data in FAQ.items():
        keyboard.add(
            InlineKeyboardButton(
                text=f"{data[0]}",
                callback_data=f"faq_{number}"),
        )
    keyboard.add(to_main)
    return keyboard.adjust(1).as_markup()


def faq_answer_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(
            text=f"Another question",
            callback_data=f"bot_faq"),
    )

    keyboard.add(to_main)
    return keyboard.adjust(2).as_markup()


async def subcategories_keyboard(cat_id: int):
    subcategories = await get_subcategories(cat_id)
    keyboard = InlineKeyboardBuilder()
    for subcategory in subcategories:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{subcategory.title}",
                callback_data=f"subcategory_{subcategory.id}"),
        )
    keyboard.add(to_main)

    return keyboard.adjust(2).as_markup()


async def products_keyboard(subcat_id: int):
    products = await get_products(subcat_id)
    keyboard = InlineKeyboardBuilder()
    for product in products:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{product.title}",
                callback_data=f"products_{product.id}"),
        )
    keyboard.add(to_main)
    return keyboard.adjust(2).as_markup()


async def product_keyboard(prod_id: int, count: int = 1):
    product = await get_product(prod_id)
    buttons = [
        [
            InlineKeyboardButton(text="+1", callback_data=f"btn_plus_{count}_{prod_id}"),
            InlineKeyboardButton(text=f"count: {count}", callback_data="do_not_handle"),
            InlineKeyboardButton(text="-1", callback_data=f"btn_minus_{count}_{prod_id}")
        ],
        [InlineKeyboardButton(text="Accept", callback_data=f"accept_{count}_{prod_id}")],
        [to_main],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard, product, count


async def cart_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="Checkout", callback_data="checkout"),
            InlineKeyboardButton(text="Delete product from cart", callback_data="delete_products")
        ],
        [to_main],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

