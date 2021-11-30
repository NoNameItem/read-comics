# Generated by Django 3.1.7 on 2021-03-13 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("volumes", "0005_auto_20210311_1130"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="volume",
            name="comicvine_matched",
        ),
        migrations.AddField(
            model_name="volume",
            name="comicvine_status",
            field=models.CharField(
                choices=[
                    ("NOT_MATCHED", "Not matched"),
                    ("QUEUED", "Waiting in queue"),
                    ("MATCHED", "Matched"),
                ],
                default="NOT_MATCHED",
                max_length=15,
            ),
        ),
    ]
