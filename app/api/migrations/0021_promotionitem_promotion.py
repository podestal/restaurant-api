# Generated by Django 4.2.16 on 2024-12-08 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_rename_discount_value_promotion_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotionitem',
            name='promotion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='api.promotion'),
            preserve_default=False,
        ),
    ]
