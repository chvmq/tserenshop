# Generated by Django 3.1.5 on 2021-02-22 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
        ('account', '0002_account_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='orders',
            field=models.ManyToManyField(blank=True, related_name='related_customer', to='shop.Order', verbose_name='Заказы покупателя'),
        ),
    ]
