# Generated by Django 4.2.16 on 2024-11-23 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_category_time_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='dishes/'),
        ),
    ]
