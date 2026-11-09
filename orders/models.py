# pyright: reportArgumentType=false, reportAttributeAccessIssue=false
# pyright: reportReturnType=false, reportOperatorIssue=false
from decimal import Decimal
from django.db import models


class OrderQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=self.model.Status.ACTIVE)

    def cancelled(self):
        return self.filter(status=self.model.Status.CANCELLED)

    def completed(self):
        return self.filter(status=self.model.Status.COMPLETED)

    def for_product(self, product):
        return self.filter(product=product)


class OrderManager(models.Manager.from_queryset(OrderQuerySet)):
    pass


class Order(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "active", "Активно"
        CANCELLED = "cancelled", "Отменено"
        COMPLETED = "completed", "Завершено"

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Товар",
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество",
        help_text="Количество единиц товара в заказе.",
    )
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Статус заказа",
    )

    objects = OrderManager()

    @property
    def is_cancelled(self) -> bool:
        return self.status == self.Status.CANCELLED

    @is_cancelled.setter
    def is_cancelled(self, value: bool) -> None:
        self.status = self.Status.CANCELLED if value else self.Status.ACTIVE

    def cancel(self) -> None:
        if self.status != self.Status.CANCELLED:
            self.status = self.Status.CANCELLED
            self.save(update_fields=["status"])
            self.product.increase_quantity(self.quantity)

    def complete(self) -> None:
        if self.status == self.Status.ACTIVE:
            self.status = self.Status.COMPLETED
            self.save(update_fields=["status"])

    @property
    def product_name(self) -> str:
        return str(self.product.name)

    @property
    def total(self) -> Decimal:
        return self.product.price * self.quantity

    def __str__(self) -> str:
        status_label = self.get_status_display().lower()
        return f"Заказ №{self.pk}: {self.product.name} ({self.quantity} шт., {status_label})"

    class Meta:

        ordering = ("id",)
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
