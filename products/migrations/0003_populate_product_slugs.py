from django.db import migrations
from django.utils.text import slugify
from unidecode import unidecode


def populate_product_slugs(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    for product in Product.objects.all().order_by("pk"):
        transliterated_name = unidecode(product.name)
        base_slug = slugify(transliterated_name) or "product"
        product.slug = f"{base_slug}-{product.pk}"
        product.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_product_is_large_product_slug_alter_product_price_and_more"),
    ]

    operations = [
        migrations.RunPython(
            populate_product_slugs,
            migrations.RunPython.noop,
        ),
    ]
