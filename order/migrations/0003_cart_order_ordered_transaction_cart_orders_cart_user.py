# Generated by Django 4.1.2 on 2022-12-22 19:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("order", "0002_order_course"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("pkid", models.BigAutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("reference", models.CharField(max_length=100)),
                (
                    "total_amount",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
            ],
            options={
                "ordering": ["-created_at", "-updated_at"],
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="order",
            name="ordered",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("pkid", models.BigAutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("transaction_ref", models.CharField(max_length=100)),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("payment_card", "Payment Card"),
                            ("bank_transfer", "Bank Transfer"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "discount",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "vat",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "total_price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                ("verified", models.BooleanField(default=False)),
                (
                    "transaction_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Pending Payment", "Pending Payment"),
                            ("Payment Completed", "Payment Completed"),
                        ],
                        default="Pending Payment",
                        max_length=200,
                        null=True,
                    ),
                ),
                (
                    "transaction_description",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "cart",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="order.cart"
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at", "-updated_at"],
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="cart",
            name="orders",
            field=models.ManyToManyField(to="order.order"),
        ),
        migrations.AddField(
            model_name="cart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]