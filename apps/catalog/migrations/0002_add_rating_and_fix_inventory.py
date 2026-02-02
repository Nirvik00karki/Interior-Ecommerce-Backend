# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        # Rename Inventory.quantity to stock
        migrations.RenameField(
            model_name='inventory',
            old_name='quantity',
            new_name='stock',
        ),
        # Add cached rating fields to Product
        migrations.AddField(
            model_name='product',
            name='average_rating',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='review_count',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
