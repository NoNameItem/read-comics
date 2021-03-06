# Generated by Django 3.0.4 on 2020-03-24 12:48

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("publishers", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="publisher",
            name="slug",
            field=django_extensions.db.fields.AutoSlugField(
                blank=True, editable=False, overwrite=True, populate_from=["name"]
            ),
        ),
    ]
