# Generated by Django 4.1.1 on 2022-10-11 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mebel_app', '0019_alter_product_color_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(max_length=20, verbose_name='Цена'),
        ),
    ]
