# Generated by Django 4.2.1 on 2023-06-22 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0011_post_comments_post_likes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="comments",
            field=models.ManyToManyField(related_name="comments", to="post.comment"),
        ),
    ]
