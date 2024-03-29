# Generated by Django 4.1.2 on 2023-02-10 14:01

import common.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0001_initial"),
        ("user", "0015_alter_bankaccount_account_balance_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="currency",
            field=models.ForeignKey(
                default=common.utils.get_default_currency,
                on_delete=django.db.models.deletion.PROTECT,
                to="common.currency",
            ),
        ),
    ]
