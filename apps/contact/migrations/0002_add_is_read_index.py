# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactsubmission',
            name='is_read',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
