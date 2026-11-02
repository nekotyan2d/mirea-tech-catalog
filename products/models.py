# pyright: reportArgumentType=false, reportAttributeAccessIssue=false
# pyright: reportReturnType=false, reportOperatorIssue=false
from decimal import Decimal
from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название категории",
    )

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        ordering = ("name",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Manufacturer(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название производителя",
    )
    country = models.CharField(
        max_length=100,
        verbose_name="Страна",
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.country})"

    class Meta:
        ordering = ("name",)
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название товара",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Категория",
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Производитель",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество на складе",
    )

    def is_in_stock(self, min_quantity: int = 1) -> bool:
        return self.quantity >= min_quantity

    def reduce_quantity(self, quantity: int) -> None:
        if quantity > self.quantity:
            raise ValueError("Недостаточно товара на складе")
        self.quantity -= quantity
        self.save(update_fields=["quantity"])

    def increase_quantity(self, quantity: int) -> None:
        self.quantity += quantity
        self.save(update_fields=["quantity"])

    @staticmethod
    def validate_price(price: float | Decimal) -> bool:
        return price >= 0

    @property
    def in_stock(self) -> bool:
        return self.quantity > 0

    @property
    def category_name(self) -> str:
        return str(self.category.name)

    @property
    def manufacturer_name(self) -> str:
        return str(self.manufacturer.name)

    @property
    def manufacturer_country(self) -> str:
        return str(self.manufacturer.country)

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.category.name}, {self.manufacturer.name}): "
            f"{self.price} руб., {self.quantity} шт."
        )

    class Meta:
        ordering = ("name",)
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
