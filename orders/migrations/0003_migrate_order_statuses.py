from django.db import migrations


def migrate_order_statuses(apps, schema_editor):
    Order = apps.get_model("orders", "Order")
    Order.objects.filter(is_cancelled=True).update(status="cancelled")
    Order.objects.filter(is_cancelled=False).update(status="active")


def reverse_order_statuses(apps, schema_editor):
    Order = apps.get_model("orders", "Order")
    Order.objects.filter(status="cancelled").update(is_cancelled=True)
    Order.objects.exclude(status="cancelled").update(is_cancelled=False)


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_order_status"),
    ]

    operations = [
        migrations.RunPython(
            migrate_order_statuses,
            reverse_order_statuses,
        ),
    ]
