# Generated by Django 3.1.5 on 2021-03-10 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("powers", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="power",
            name="comicvine_last_match",
            field=models.DateTimeField(null=True),
        ),
    ]
