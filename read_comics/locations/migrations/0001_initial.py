# Generated by Django 3.0.2 on 2020-03-23 01:33

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("comicvine_id", models.IntegerField(unique=True)),
                ("comicvine_url", models.URLField(max_length=1000)),
                ("comicvine_matched", models.BooleanField(default=False)),
                ("created_dt", models.DateTimeField(auto_now_add=True)),
                ("modified_dt", models.DateTimeField(auto_now_add=True)),
                ("name", models.TextField()),
                ("aliases", models.TextField(null=True)),
                ("short_description", models.TextField(null=True)),
                ("html_description", models.TextField(null=True)),
                ("thumb_url", models.URLField(max_length=1000, null=True)),
                ("image_url", models.URLField(max_length=1000, null=True)),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=["name"]),
                ),
            ],
            options={
                "ordering": ("name",),
            },
        ),
    ]
