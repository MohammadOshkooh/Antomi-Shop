# Generated by Django 4.0.4 on 2022-05-24 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_cart_item'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': 'ایتم های سبد خرید', 'verbose_name_plural': 'ایتم های سبد های خرید مشتریان'},
        ),
        migrations.AlterField(
            model_name='cart',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
    ]
