# Generated by Django 4.2.1 on 2023-06-22 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0003_rename_user_post_user_id_alter_post_post_id"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="post",
            table="post",
        ),
    ]
