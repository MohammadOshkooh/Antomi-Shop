# Generated by Django 4.0.4 on 2022-05-15 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_gallery_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=200, verbose_name='برچسب')),
            ],
            options={
                'verbose_name': 'برچسب',
                'verbose_name_plural': 'برچسب ها',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(blank=True, to='shop.producttag'),
        ),
    ]
