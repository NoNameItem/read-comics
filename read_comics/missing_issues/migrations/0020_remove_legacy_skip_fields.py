from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("missing_issues", "0019_missingissue_skip_until")]

    operations = [
        migrations.RemoveField(model_name="missingissue", name="skip_date"),
        migrations.RemoveField(model_name="missingissue", name="skip"),
    ]
