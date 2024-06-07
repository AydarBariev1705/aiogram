from typing import List

from sqlalchemy import ForeignKey, Integer, String, Numeric, Text, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
import datetime

from database import Base


class Category(Base):
    """
    Модель категории продукта
    """
    __tablename__ = "aiogramapp_category"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        index=True,
    )

    def __str__(self) -> str:
        return f"{self.title!r}"


class Subcategory(Base):
    """
    Модель подкатегории продукта
    """
    __tablename__ = "aiogramapp_subcategory"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        index=True,
    )
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("aiogramapp_category.id"),
    )

    def __str__(self) -> str:
        return f"{self.title!r}"


class Product(Base):
    """
    Модель продукта
    """
    __tablename__ = "aiogramapp_product"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    price = mapped_column(
        Numeric(8, 2),
        default=1,
        nullable=False,
    )

    subcategory_id: Mapped[int] = mapped_column(
        ForeignKey("aiogramapp_subcategory.id"),
    )

    image: Mapped[str] = mapped_column(String, nullable=True)

    def __str__(self):
        return self.title


class Tguser(Base):
    """
    Модель пользователя
    """
    __tablename__ = "aiogramapp_tguser"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    tg_id: Mapped[str] = mapped_column(
        Integer, nullable=False,
    )


class Basket(Base):
    """
    Модель корзины продукта
    """
    __tablename__ = "aiogramapp_basket"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    tg_id: Mapped[int] = mapped_column(
        Integer,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("aiogramapp_product.id"),
    )
    quantity: Mapped[str] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )


class Newsletter(Base):
    """
    Модель рассылки
    """
    __tablename__ = "aiogramapp_newsletter"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    message: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    tg_user_list: Mapped[List] = mapped_column(ARRAY(Integer))

    created_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow,
        nullable=True,

    )
