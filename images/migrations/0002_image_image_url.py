# Generated by Django 4.1.7 on 2023-03-09 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="image_url",
            field=models.URLField(default="http://127.0.0.1:8000/admin/images/image/"),
        ),
    ]