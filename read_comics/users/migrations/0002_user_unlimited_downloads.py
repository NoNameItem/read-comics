# Generated by Django 3.2.9 on 2022-05-13 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='unlimited_downloads',
            field=models.BooleanField(default=False),
        ),
    ]
