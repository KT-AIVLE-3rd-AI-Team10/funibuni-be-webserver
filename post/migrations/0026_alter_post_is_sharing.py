# Generated by Django 4.2.1 on 2023-06-26 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0025_alter_post_is_sharing"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="is_sharing",
            field=models.BooleanField(default=False),
        ),
    ]