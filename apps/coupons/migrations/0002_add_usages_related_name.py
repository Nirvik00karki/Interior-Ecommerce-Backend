# Generated manually

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couponusage',
            name='coupon',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name='usages',
                to='coupons.coupon'
            ),
        ),
    ]
