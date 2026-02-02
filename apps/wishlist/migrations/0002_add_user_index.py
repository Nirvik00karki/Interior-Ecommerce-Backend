# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='user',
            field=models.ForeignKey(
                db_index=True,
                on_delete=models.deletion.CASCADE,
                related_name='wishlist_items',
                to='accounts.user'
            ),
        ),
    ]
