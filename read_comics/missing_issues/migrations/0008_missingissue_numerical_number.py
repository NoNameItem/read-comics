# Generated by Django 3.2.9 on 2021-12-13 03:48
import re

from django.db import migrations, models


def get_numerical_number(missing_issue):
    if missing_issue.number:
        if missing_issue.number == '½':
            return 0.5
        else:
            r = re.compile(r'^\d+(\.\d+)?')
            match = r.match(missing_issue.number)
            if match:
                return float(match.group(0))
            else:
                return 0
    else:
        return None


def populate_numberic_number(apps, schema_editor):
    MissingIssue = apps.get_model('missing_issues', 'MissingIssue')
    for missing_issue in MissingIssue.objects.all():
        missing_issue.numerical_number = get_numerical_number(missing_issue)
        missing_issue.save()


class Migration(migrations.Migration):

    dependencies = [
        ('missing_issues', '0007_auto_20211207_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='missingissue',
            name='numerical_number',
            field=models.FloatField(null=True),
        ),
        migrations.RunPython(populate_numberic_number, reverse_code=migrations.RunPython.noop),
    ]