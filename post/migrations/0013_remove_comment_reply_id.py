# Generated by Django 4.2.1 on 2023-06-20 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0012_comment_reply_id_delete_reply"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="reply_id",
        ),
    ]