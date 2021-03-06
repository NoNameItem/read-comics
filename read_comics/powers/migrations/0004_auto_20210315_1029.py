# Generated by Django 3.1.7 on 2021-03-15 10:29

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("powers", "0003_auto_20210313_1737"),
    ]

    operations = [
        migrations.AlterField(
            model_name="power",
            name="slug",
            field=django_extensions.db.fields.AutoSlugField(
                blank=True, editable=False, overwrite=True, populate_from=["name"]
            ),
        ),
    ]
