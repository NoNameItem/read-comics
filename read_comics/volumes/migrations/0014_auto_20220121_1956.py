# Generated by Django 3.2.9 on 2022-01-21 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volumes', '0013_alter_volume_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='volume',
            name='first_issue_number',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='volume',
            name='last_issue_number',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
