# Generated by Django 4.1.2 on 2023-02-10 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0001_initial"),
        ("courses", "0008_course_translation_alter_course_content_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="currency",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="common.currency",
            ),
        ),
        migrations.DeleteModel(
            name="Currency",
        ),
    ]
