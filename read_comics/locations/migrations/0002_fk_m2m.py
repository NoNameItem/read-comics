# Generated by Django 3.0.2 on 2020-03-24 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("issues", "0002_fk_m2m"),
        ("locations", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="location",
            name="first_issue",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="first_appearance_locations",
                to="issues.Issue",
            ),
        ),
        migrations.AddField(
            model_name="location",
            name="first_issue_name",
            field=models.TextField(null=True),
        ),
    ]
