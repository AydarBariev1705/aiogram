from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.

def images_directory_path(instance: 'Product', filename: str) -> str:
    """
    Путь для загрузки изображения через кастомную функцию

    :param instance: Product
    :param filename: str
    :return: str
    """
    return (f'products/'
            f'product_{instance.pk}/'
            f'{filename}')


class Category(models.Model):
    """
    Модель категории продукта
    """

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['pk', 'title']

    title = models.CharField(
        max_length=40,
        db_index=True,
    )

    def __str__(self) -> str:
        return f"{self.title!r}"


class Subcategory(models.Model):
    """
    Модель подкатегории продукта
    """

    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'
        ordering = ['pk', 'title']

    title = models.CharField(
        max_length=40,
        db_index=True,
    )
    parent = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
    )

    def __str__(self) -> str:
        return f"{self.title!r}"


class Product(models.Model):
    """
    Модель продукта
    """

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['pk', 'title']

    def __str__(self):
        return self.title

    title = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )
    description = models.TextField(
        null=False,
        blank=True,
    )
    price = models.DecimalField(
        default=1,
        max_digits=8,
        decimal_places=2,
        null=False,
    )

    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
    )
    # image = models.ImageField(
    #     null=True,
    #     blank=True,
    #     upload_to=images_directory_path,
    # )
    image = models.CharField(
        null=True,
        blank=True,

    )


class Tguser(models.Model):
    """
    Модель пользователя
    """
    tg_id = models.BigIntegerField(
        null=False,
    )


class Basket(models.Model):
    """
    Модель корзины
    """
    tg_id = models.BigIntegerField(
        null=False,
        default=1,
    )

    product = models.ForeignKey(
        Product,
        related_name='products',
        on_delete=models.PROTECT)

    quantity = models.IntegerField(
        default=1,
        null=False,
    )


class Newsletter(models.Model):
    """
    Модель рассылки
    """
    message = models.TextField(
        null=False,
        blank=True,
    )
    tg_user_list = ArrayField(models.BigIntegerField(null=True, blank=True), blank=True, )
    created_at = models.DateTimeField(auto_now_add=True)


class Totalcost(models.Model):
    total_cost = models.IntegerField(
        default=1,
        null=False,
    )
    tg_id = models.BigIntegerField(
        null=False,
        default=1,
    )


class Temporary(models.Model):
    product_id = models.IntegerField(
        default=1,
        null=False,
    )
    tg_id = models.BigIntegerField(
        null=False,
        default=1,
    )
