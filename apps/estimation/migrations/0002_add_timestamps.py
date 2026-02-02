# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estimation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='estimationcategory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='estimationcategory',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
