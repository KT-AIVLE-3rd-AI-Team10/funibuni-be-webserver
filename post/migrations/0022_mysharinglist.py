# Generated by Django 4.2.1 on 2023-06-24 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("post", "0021_favoritepost"),
    ]

    operations = [
        migrations.CreateModel(
            name="MySharingList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "posts",
                    models.ManyToManyField(
                        related_name="sharing_lists", to="post.post"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sharing_list",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "my_sharing_list",
            },
        ),
    ]
