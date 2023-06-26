# Generated by Django 4.2 on 2023-06-26 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("waste", "0002_preprocessedimages_delete_wasteinfo"),
    ]

    operations = [
        migrations.CreateModel(
            name="UrlImages",
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
                ("image_title", models.TextField(default="testt.jpg", null=True)),
                ("image_url", models.FilePathField(default="media/testt.jpg")),
            ],
            options={
                "db_table": "url_images",
            },
        ),
        migrations.DeleteModel(
            name="PreprocessedImages",
        ),
    ]
