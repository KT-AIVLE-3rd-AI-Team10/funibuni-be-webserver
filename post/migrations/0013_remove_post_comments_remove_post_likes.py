# Generated by Django 4.2.1 on 2023-06-22 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0012_alter_post_comments"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="comments",
        ),
        migrations.RemoveField(
            model_name="post",
            name="likes",
        ),
    ]