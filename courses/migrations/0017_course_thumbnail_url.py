# Generated by Django 4.1.2 on 2022-12-13 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0016_alter_video_embedded_link_alter_video_video_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="thumbnail_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]
