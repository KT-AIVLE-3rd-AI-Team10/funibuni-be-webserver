# Generated by Django 4.2.1 on 2023-06-22 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0002_rename_user_id_post_user_alter_post_post_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="user",
            new_name="user_id",
        ),
        migrations.AlterField(
            model_name="post",
            name="post_id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]