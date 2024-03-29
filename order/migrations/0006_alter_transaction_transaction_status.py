# Generated by Django 4.1.2 on 2023-01-09 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0005_transaction_payment_provider_delete_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="transaction_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Pending Payment", "Pending Payment"),
                    ("Payment Completed", "Payment Completed"),
                    ("Payment Failed", "Payment Failed"),
                    ("Payment Error", "Payment Error"),
                ],
                default="Pending Payment",
                max_length=200,
                null=True,
            ),
        ),
    ]
