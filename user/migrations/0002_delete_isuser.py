# Generated by Django 4.1.2 on 2022-10-29 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="IsUser",
        ),
    ]