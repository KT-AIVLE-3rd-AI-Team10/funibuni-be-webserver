# Generated by Django 4.2.1 on 2023-06-21 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_rename_id_user_user_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="user_id",
            new_name="id",
        ),
    ]
