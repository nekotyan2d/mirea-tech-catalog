# pyright: reportArgumentType=false, reportAttributeAccessIssue=false
# pyright: reportReturnType=false, reportOperatorIssue=false
from decimal import Decimal
from django.db import models


class Order(models.Model):
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Товар",
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество",
    )
    is_cancelled = models.BooleanField(
        default=False,
        verbose_name="Заказ отменен",
    )

    def cancel(self) -> None:
        if not self.is_cancelled:
            self.is_cancelled = True
            self.save(update_fields=["is_cancelled"])
            self.product.increase_quantity(self.quantity)

    @property
    def product_name(self) -> str:
        return str(self.product.name)

    @property
    def total(self) -> Decimal:
        return self.product.price * self.quantity

    def __str__(self) -> str:
        status = "отменен" if self.is_cancelled else "активен"
        return f"Заказ №{self.pk}: {self.product.name} ({self.quantity} шт., {status})"

    class Meta:
        ordering = ("id",)
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
