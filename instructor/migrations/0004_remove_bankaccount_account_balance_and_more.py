# Generated by Django 4.1.2 on 2023-03-17 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("instructor", "0003_instructor_accept_terms_and_conditions_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bankaccount",
            name="account_balance",
        ),
        migrations.AddField(
            model_name="instructor",
            name="account_balance",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
