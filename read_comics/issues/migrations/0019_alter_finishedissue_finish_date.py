# Generated by Django 3.2.9 on 2022-02-16 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("issues", "0018_alter_issue_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="finishedissue",
            name="finish_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
