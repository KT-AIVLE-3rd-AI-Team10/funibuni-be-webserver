# Generated by Django 4.2.1 on 2023-06-19 17:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("post", "0003_delete_comment"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("Comment_id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateField(auto_now_add=True)),
                ("comment", models.TextField()),
                (
                    "Post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="post.post"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]