# Generated by Django 3.2.9 on 2021-12-12 00:38

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("powers", "0007_alter_power_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="power",
            name="slug",
            field=django_extensions.db.fields.AutoSlugField(
                blank=True, editable=False, max_length=1000, overwrite=True, populate_from=["name"], unique=True
            ),
        ),
    ]
