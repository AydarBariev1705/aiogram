from sqlalchemy import ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column

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
    __tablename__ = "aiogramApp_subcategory"

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
        ForeignKey("aiogramapp_category.id")
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

    Description: Mapped[str] = mapped_column(String)
    price = mapped_column(Numeric(8, 2), default=1, nullable=False)
    count: Mapped[str] = mapped_column(Integer, default=1, nullable=False)
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("aiogramApp_subcategory.id"))

    image: Mapped[str] = mapped_column(String, nullable=True)

    def __str__(self):
        return self.title
