from aiogram.types import Message

from database import async_session
from sqlalchemy import select
from models import Category, Subcategory, Product, Tguser, Basket


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(Tguser).where(Tguser.tg_id == tg_id))
        if not user:
            session.add(Tguser(tg_id=tg_id))
            await session.commit()


async def add_to_basket(tg_id: int, product_id: int):
    async with async_session() as session:
        basket = await session.scalar(select(Basket).where(
            Basket.tg_user_id == tg_id,
            Basket.product_id == product_id,
        )
        )
        if not basket:
            session.add(Basket(tg_user_id=tg_id, product_id=product_id))
            await session.commit()


async def get_users():
    async with async_session() as session:
        users = await session.scalars(select(Tguser))
        return users


async def get_categories():
    async with async_session() as session:
        categories = await session.scalars(select(Category))
    return categories


async def get_subcategories(cat_id: int):
    async with async_session() as session:
        subcategories = await session.scalars(select(Subcategory).where(Subcategory.parent_id == cat_id))
    return subcategories


async def get_products(subcat_id: int):
    async with async_session() as session:
        products = await session.scalars(select(Product).where(Product.subcategory_id == subcat_id))
    return products
