# Generated by Django 4.2.16 on 2024-11-25 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_dish_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_type',
            field=models.CharField(choices=[('I', 'Dine in'), ('D', 'Delivery'), ('T', 'Take out')], default='I', max_length=1),
        ),
    ]
