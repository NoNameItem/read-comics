# Generated by Django 3.2.9 on 2025-02-26 23:22

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0019_alter_finishedissue_finish_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='variant_covers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(max_length=1000, null=True), default=list, size=None),
        ),
    ]
