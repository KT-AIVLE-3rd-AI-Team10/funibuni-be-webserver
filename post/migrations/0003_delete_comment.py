# Generated by Django 4.2.1 on 2023-06-19 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0002_comment"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Comment",
        ),
    ]