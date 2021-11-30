# Generated by Django 3.1.7 on 2021-03-15 10:29

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0006_team_first_issue_comicvine_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="slug",
            field=django_extensions.db.fields.AutoSlugField(
                blank=True,
                editable=False,
                overwrite=True,
                populate_from=["get_publisher_name", "name"],
            ),
        ),
    ]
