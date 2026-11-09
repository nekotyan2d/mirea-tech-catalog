# pyright: reportArgumentType=false, reportAttributeAccessIssue=false
# pyright: reportReturnType=false, reportOperatorIssue=false
from decimal import Decimal
from django.db import models
from django.db.models import Case, Value, When
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


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
        help_text="Укажите цену товара в рублях.",
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество на складе",
        help_text="Укажите количество товара на складе.",
    )
    is_large = models.GeneratedField(
        expression=Case(
            When(quantity__gte=10, then=Value(True)),
            default=Value(False),
            output_field=models.BooleanField(),
        ),
        output_field=models.BooleanField(),
        db_persist=True,
        verbose_name="Крупный остаток",
    )
    slug = models.SlugField(
        max_length=220,
        unique=True,
        editable=False,
        verbose_name="URL-идентификатор",
    )

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            transliterated_name = unidecode(self.name)
            base_slug = slugify(transliterated_name) or "product"
            if self.pk:
                self.slug = f"{base_slug}-{self.pk}"
            else:
                super().save(*args, **kwargs)
                self.slug = f"{base_slug}-{self.pk}"
                super().save(update_fields=["slug"])
                return
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("products:detail", kwargs={"slug": self.slug})

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
