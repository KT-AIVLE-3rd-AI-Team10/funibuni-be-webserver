# Generated by Django 4.2 on 2023-06-27 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("waste", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="WasteSpec",
            fields=[
                ("waste_spec_id", models.AutoField(primary_key=True, serialize=False)),
                ("index_large_category", models.IntegerField()),
                ("city", models.CharField(max_length=50)),
                ("district", models.CharField(max_length=50)),
                ("top_category", models.CharField(max_length=50)),
                ("large_category", models.CharField(max_length=50)),
                ("small_category", models.CharField(max_length=50)),
                ("size_range", models.CharField(max_length=50, null=True)),
                ("is_exists_small_cat_model", models.BooleanField(default=True)),
                ("type", models.CharField(max_length=50)),
                ("fee", models.IntegerField()),
            ],
        ),
    ]
