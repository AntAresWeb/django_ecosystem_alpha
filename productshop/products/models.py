from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver

import core.constants as const

User = get_user_model()


class BaseCategory(models.Model):
    name = models.CharField(
        max_length=const.LENGTH_STRING_100,
        verbose_name='Наименование'
    )
    slug = models.SlugField(
        max_length=const.LENGTH_STRING_50,
        unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(BaseCategory):
    class Meta:
        verbose_name = 'Категория продукта'
        verbose_name_plural = 'Категории продуктов'


class Subcategory(BaseCategory):
    category = models.ForeignKey(
        Category,
        related_name='subcategories',
        on_delete=models.CASCADE,
        verbose_name='Относится к категории'
    )

    class Meta:
        verbose_name = 'Подкатегория продукта'
        verbose_name_plural = 'Подкатегории продуктов'


class Product(models.Model):
    subcategory = models.ForeignKey(
        Subcategory,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name='Относится к подкатегории'
    )
    slug = models.SlugField(
        max_length=const.LENGTH_STRING_50,
        unique=True,
        verbose_name='Слаг',
    )
    name = models.CharField(
        max_length=const.LENGTH_STRING_200,
        verbose_name='Наименование продукта'
    )
    price = models.FloatField(
        validators=(
            MinValueValidator(const.MIN_PRICE),
            MaxValueValidator(const.MAX_PRICE),
        ),
        verbose_name='Цена продукта'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='shoppingcarts',
        on_delete=models.CASCADE,
        verbose_name='Владелец корзины'
    )
    product = models.ForeignKey(
        Product,
        related_name='shoppingcarts',
        on_delete=models.CASCADE,
        verbose_name='Список продуктов'
    )
    quantity = models.FloatField(
        validators=(
            MinValueValidator(const.MIN_PRICE),
            MaxValueValidator(const.MAX_PRICE),
        ),
        verbose_name='Цена продукта'
    )

    class Meta:
        verbose_name = 'Корзина продуктов'
        verbose_name_plural = 'Корзины продуктов'

    def __str__(self):
        return f'Корзина пользователя: {self.owner}'


class Image(models.Model):
    file = models.FileField(
        upload_to='images',
        unique=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )

    class Meta:
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продуктов'
        constraints = (
            models.UniqueConstraint(
                name='product_image',
                fields=('file', 'product',),
            ),
        )

    def __str__(self):
        return f'Изображение продукта: {self.product}'


@receiver(post_delete, sender=Image)
def image_file_delete(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(False)
