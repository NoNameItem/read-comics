# Generated by Django 3.0.4 on 2020-03-25 16:21

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("issues", "0003_rename_objects_to_object_in"),
    ]

    operations = [
        migrations.AlterField(
            model_name="issue",
            name="slug",
            field=django_extensions.db.fields.AutoSlugField(
                blank=True, editable=False, overwrite=True, populate_from=["name"]
            ),
        ),
    ]
