# Generated by Django 4.1.2 on 2022-12-22 13:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0004_rename_finished_enrollment_completed"),
    ]

    operations = [
        migrations.AddField(
            model_name="enrollment",
            name="completed_on",
            field=models.DateField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
