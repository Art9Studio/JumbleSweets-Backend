# Generated by Django 2.1.2 on 2018-10-27 18:28

from django.db import migrations
import django_prices.models


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0014_auto_20180920_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingmethod',
            name='maximum_order_price',
            field=django_prices.models.MoneyField(blank=True, currency='UAH', decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='shippingmethod',
            name='minimum_order_price',
            field=django_prices.models.MoneyField(blank=True, currency='UAH', decimal_places=2, default=0, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='shippingmethod',
            name='price',
            field=django_prices.models.MoneyField(currency='UAH', decimal_places=2, default=0, max_digits=12),
        ),
    ]
