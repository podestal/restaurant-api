# Generated by Django 4.2.16 on 2024-12-07 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_alter_orderitem_dish_alter_orderitem_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('discount_type', models.CharField(choices=[('P', 'Percentage'), ('F', 'Fixed Amount')], default='P', max_length=1)),
                ('discount_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('applicable_categories', models.ManyToManyField(blank=True, related_name='promotions', to='api.category')),
                ('applicable_dishes', models.ManyToManyField(blank=True, related_name='promotions', to='api.dish')),
            ],
        ),
        migrations.CreateModel(
            name='DiscountCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('max_uses', models.PositiveIntegerField(default=1)),
                ('uses', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('promotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discount_codes', to='api.promotion')),
            ],
        ),
    ]