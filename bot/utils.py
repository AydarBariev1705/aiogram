import pandas as pd
import datetime
import os

from config import EXEL_FILENAME, SHEET_NAME
from database import async_session
from sqlalchemy import select, delete
from models import Category, Subcategory, Product, Tguser, Basket, Newsletter


async def set_user(tg_id: int) -> None:
    """Функция для записи пользователя в БД"""
    async with async_session() as session:
        user = await session.scalar(select(Tguser).where(Tguser.tg_id == tg_id))
        if not user:
            session.add(Tguser(tg_id=tg_id))
            await session.commit()


async def create_newsletter(tg_user_list: list, message: str) -> None:
    """Функция для записи рассылки в БД"""
    async with async_session() as session:
        session.add(Newsletter(tg_user_list=tg_user_list, message=message))
        await session.commit()


async def get_users():
    """Функция для извлечения данных о пользователях"""
    async with async_session() as session:
        users = await session.scalars(select(Tguser))
        return users


async def get_categories():
    """Функция для извлечения данных о категориях"""
    async with async_session() as session:
        categories = await session.scalars(select(Category))
    return categories


async def get_subcategories(cat_id: int):
    """Функция для извлечения данных о подкатегориях"""
    async with async_session() as session:
        subcategories = await session.scalars(select(Subcategory).where(Subcategory.parent_id == cat_id))
    return subcategories


async def get_products(subcat_id: int):
    """Функция для извлечения данных о продуктах"""
    async with async_session() as session:
        products = await session.scalars(select(Product).where(Product.subcategory_id == subcat_id))
    return products


async def get_product(prod_id: int):
    """Функция для извлечения данных о продукте"""
    async with async_session() as session:
        product = await session.scalar(select(Product).where(Product.id == prod_id))
    return product


async def set_or_create_basket(tg_id: int, product_id: int, quantity: int):
    """Функция для изменения или создания Корзины"""
    async with async_session() as session:
        basket = await session.scalar(select(Basket).where(
            Basket.tg_id == tg_id).where(
            Basket.product_id == product_id,
        ),
        )
        if not basket:
            session.add(Basket(tg_id=tg_id, product_id=product_id, quantity=quantity))
            await session.commit()
        else:
            basket.quantity += quantity
            await session.commit()


async def get_cart(tg_id: int):
    """Функция для формирования данных о корзине пользователя"""
    async with async_session() as session:
        cart = await session.scalars(select(Basket).where(Basket.tg_id == tg_id))
        if cart:
            return cart
        if not cart:
            return None


async def del_product(tg_id: int, product_id):
    """Функция для удаления товара из корзины"""
    async with async_session() as session:
        query = delete(Basket).where(Basket.tg_id == tg_id).where(Basket.product_id == product_id)
        await session.execute(query)
        await session.commit()


async def clear_cart(tg_id: int, ):
    """Функция для удаления всех товаров из корзины"""
    async with async_session() as session:
        query = delete(Basket).where(Basket.tg_id == tg_id)
        await session.execute(query)
        await session.commit()


async def set_total_cost(cart):
    """Функция для уточнения полной стоимости товаров в корзине"""
    total_cost = 0
    message_string = ''
    for obj in cart:
        product = await get_product(obj.product_id)
        total_summ_for_product = obj.quantity * product.price
        total_cost += total_summ_for_product
        message_string += (f"*{product.title}*\n"
                           f"quantity in cart: {obj.quantity}\n"
                           f"price: {obj.quantity * product.price}\n")
    return total_cost, message_string


async def add_to_exel(data_dict: dict):
    """Функция для записи о заказе в EXEL файл"""
    str_address = ', '.join(data_dict['order_info']['shipping_address'].values())
    final_dict = {
        'name': [data_dict['order_info']['name']],
        'phone_number': [data_dict['order_info']['phone_number']],
        'total_amount': [int(data_dict['total_amount']) // 100],
        'currency': [data_dict['currency']],
        'telegram_payment_charge_id': [data_dict['telegram_payment_charge_id']],
        'provider_payment_charge_id': [data_dict['provider_payment_charge_id']],
        'shipping_address': [str_address],
        'date': datetime.datetime.now()
    }
    df_new = pd.DataFrame(final_dict, index=[0])
    if not os.path.exists(f'{EXEL_FILENAME}'):
        df_old = pd.DataFrame({})
    else:
        df_old = pd.read_excel(EXEL_FILENAME)
    df_final = pd.concat([df_old, df_new])

    df_final.to_excel(excel_writer=f'{EXEL_FILENAME}', sheet_name=SHEET_NAME, index=False)
