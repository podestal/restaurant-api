# Generated by Django 4.2.16 on 2024-11-12 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_table_seats'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='bill',
        ),
        migrations.DeleteModel(
            name='Bill',
        ),
    ]