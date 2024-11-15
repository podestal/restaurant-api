# Generated by Django 4.2.16 on 2024-11-15 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_remove_orderitem_table_alter_orderitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('S', 'Served'), ('C', 'Completed')], default='P', max_length=1),
        ),
    ]
