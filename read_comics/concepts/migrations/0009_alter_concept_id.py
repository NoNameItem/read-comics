# Generated by Django 3.2 on 2021-04-08 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("concepts", "0008_auto_20210329_2319"),
    ]

    operations = [
        migrations.AlterField(
            model_name="concept",
            name="id",
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
        ),
    ]
