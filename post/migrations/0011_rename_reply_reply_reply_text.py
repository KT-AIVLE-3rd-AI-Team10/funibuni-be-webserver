# Generated by Django 4.2.1 on 2023-06-20 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0010_reply"),
    ]

    operations = [
        migrations.RenameField(
            model_name="reply",
            old_name="reply",
            new_name="reply_text",
        ),
    ]
