# Generated by Django 4.2.1 on 2023-06-22 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_rename_user_id_user_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="id",
            new_name="user_id",
        ),
    ]
