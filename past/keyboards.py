# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from aiogram.utils.keyboard import InlineKeyboardBuilder
# from utils import get_categories, get_subcategories, get_products
#
#
# def main_keyboard():
#     buttons = [
#         [
#             InlineKeyboardButton(text="Categories", callback_data="bot_categories"),
#             InlineKeyboardButton(text="Cart", callback_data="bot_cart")
#         ],
#         [InlineKeyboardButton(text="FAQ", callback_data="bot_faq")]
#     ]
#     keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
#     return keyboard
#
#
# to_main = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(
#                 text='To main menu',
#                 callback_data='to_main'
#             )
#         ]
#     ]
# )
#
#
# async def categories_keyboard():
#     categories = await get_categories()
#     keyboard = InlineKeyboardBuilder()
#     for category in categories:
#         keyboard.add(
#             InlineKeyboardButton(
#                 text=f"{category.title}",
#                 callback_data=f"category_{category.id}")
#         )
#
#     return keyboard.adjust(2).as_markup()
#
#
# async def subcategories_keyboard(cat_id: int):
#     subcategories = await get_subcategories(cat_id)
#     keyboard = InlineKeyboardBuilder()
#     for subcategory in subcategories:
#         keyboard.add(
#             InlineKeyboardButton(
#                 text=f"{subcategory.title}",
#                 callback_data=f"subcategory_{subcategory.id}")
#         )
#
#     return keyboard.adjust(2).as_markup()
#
#
# async def products_keyboard(subcat_id: int):
#     products = await get_products(subcat_id)
#     keyboard = InlineKeyboardBuilder()
#     for product in products:
#         keyboard.add(
#             InlineKeyboardButton(
#                 text=f"{product.title}\n {product.description}",
#                 callback_data=f"subcategory_{product.id}")
#         )
#     return keyboard.adjust(1).as_markup()
