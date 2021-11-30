# Generated by Django 3.1.7 on 2021-03-29 23:19

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0005_auto_20210315_1205"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="slug",
            field=django_extensions.db.fields.AutoSlugField(
                blank=True,
                editable=False,
                max_length=1000,
                overwrite=True,
                populate_from=["name"],
            ),
        ),
    ]
