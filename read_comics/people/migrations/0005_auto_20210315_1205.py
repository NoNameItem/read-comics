# Generated by Django 3.1.7 on 2021-03-15 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0004_auto_20210315_1029"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="comicvine_url",
            field=models.URLField(max_length=1000, null=True),
        ),
    ]
