# Generated by Django 4.1.2 on 2022-10-07 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mebel_app', '0013_remove_favouriteproducts_product_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FavouriteProducts',
        ),
    ]
