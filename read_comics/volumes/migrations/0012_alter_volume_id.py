# Generated by Django 3.2 on 2021-04-08 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("volumes", "0011_auto_20210405_1107"),
    ]

    operations = [
        migrations.AlterField(
            model_name="volume",
            name="id",
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
        ),
    ]
