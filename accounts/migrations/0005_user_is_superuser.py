# Generated by Django 4.2.1 on 2023-06-15 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_blacklistedtoken"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_superuser",
            field=models.BooleanField(default=False),
        ),
    ]