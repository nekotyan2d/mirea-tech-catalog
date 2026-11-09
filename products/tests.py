from decimal import Decimal
from django.contrib import admin
from django.test import Client, TestCase
from django.urls import reverse

from .models import Category, Manufacturer, Product


class ProductModelAndViewsTest(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name="Тестовая категория")
        self.manufacturer = Manufacturer.objects.create(
            name="Тестовый производитель",
            country="Россия",
        )
        self.product = Product.objects.create(
            name="Ноутбук Тестовый 100",
            category=self.category,
            manufacturer=self.manufacturer,
            price=Decimal("45000.00"),
            quantity=12,
        )

    def test_slug_auto_generation_and_absolute_url(self) -> None:
        self.assertTrue(bool(self.product.slug))
        self.assertIn("noutbuk-testov", self.product.slug)
        expected_url = reverse("products:detail", kwargs={"slug": self.product.slug})
        self.assertEqual(self.product.get_absolute_url(), expected_url)

    def test_product_detail_view_by_slug(self) -> None:
        client = Client()

        response = client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_generated_field_is_large(self) -> None:
        self.product.refresh_from_db()
        self.assertTrue(self.product.is_large)

        self.product.quantity = 4
        self.product.save()
        self.product.refresh_from_db()
        self.assertFalse(self.product.is_large)

    def test_context_processor_in_template(self) -> None:
        client = Client()
        response = client.get(reverse("products:list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["site_name"], "Tech Catalog")
        self.assertGreaterEqual(response.context["products_count"], 1)

    def test_admin_registration(self) -> None:
        self.assertIn(Product, admin.site._registry)
        model_admin = admin.site._registry[Product]
        self.assertIn("quantity", model_admin.list_editable)
        self.assertIn("name", model_admin.search_fields)
        self.assertTrue(model_admin.view_on_site)
