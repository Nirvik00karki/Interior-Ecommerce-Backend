# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.OneToOneField(
                db_index=True,
                on_delete=models.deletion.CASCADE,
                related_name='cart',
                to='accounts.user'
            ),
        ),
    ]
