# Generated by Django 3.0.4 on 2020-03-25 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("volumes", "0002_fk_m2m"),
        ("issues", "0004_slug_overwrite_true"),
    ]

    operations = [
        migrations.AlterField(
            model_name="issue",
            name="volume",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="issues",
                to="volumes.Volume",
            ),
        ),
    ]
