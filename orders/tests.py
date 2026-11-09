from decimal import Decimal
from django.contrib import admin
from django.test import Client, TestCase
from django.urls import reverse

from products.models import Category, Manufacturer, Product
from .models import Order


class OrderModelAndViewsTest(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name="Тестовая категория")
        self.manufacturer = Manufacturer.objects.create(
            name="Тестовый производитель",
            country="Россия",
        )
        self.product = Product.objects.create(
            name="Монитор Тестовый",
            category=self.category,
            manufacturer=self.manufacturer,
            price=Decimal("20000.00"),
            quantity=10,
        )
        self.order = Order.objects.create(
            product=self.product,
            quantity=2,
            status=Order.Status.ACTIVE,
        )

    def test_status_choices_and_manager(self) -> None:
        self.assertEqual(self.order.status, Order.Status.ACTIVE)
        self.assertFalse(self.order.is_cancelled)
        self.assertTrue(Order.objects.active().filter(pk=self.order.pk).exists())

        self.order.complete()
        self.assertEqual(self.order.status, Order.Status.COMPLETED)
        self.assertTrue(Order.objects.completed().filter(pk=self.order.pk).exists())
        self.assertFalse(Order.objects.active().filter(pk=self.order.pk).exists())

        self.order.status = Order.Status.ACTIVE
        self.order.save()
        initial_stock = self.product.quantity
        self.order.cancel()
        self.order.refresh_from_db()
        self.product.refresh_from_db()
        self.assertEqual(self.order.status, Order.Status.CANCELLED)
        self.assertTrue(self.order.is_cancelled)
        self.assertEqual(self.product.quantity, initial_stock + 2)
        self.assertTrue(Order.objects.cancelled().filter(pk=self.order.pk).exists())

    def test_order_views(self) -> None:
        client = Client()
        resp_list = client.get(reverse("orders:list"))
        self.assertEqual(resp_list.status_code, 200)

        resp_active = client.get(f"{reverse('orders:list')}?status=active")
        self.assertEqual(resp_active.status_code, 200)

        resp_detail = client.get(reverse("orders:detail", kwargs={"order_id": self.order.pk}))
        self.assertEqual(resp_detail.status_code, 200)
        self.assertContains(resp_detail, f"Заказ №{self.order.pk}")

        resp_stats = client.get(reverse("orders:statistics"))
        self.assertEqual(resp_stats.status_code, 200)
        self.assertIn("stats", resp_stats.context)

    def test_admin_registration(self) -> None:
        self.assertIn(Order, admin.site._registry)
        model_admin = admin.site._registry[Order]
        self.assertIn("status", model_admin.list_filter)
        self.assertIn("cancel_orders", model_admin.actions)
        self.assertIn("restore_orders", model_admin.actions)
