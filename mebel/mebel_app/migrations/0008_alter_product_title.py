# Generated by Django 4.1.1 on 2022-09-16 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mebel_app', '0007_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=255, unique=True, verbose_name='Название товара'),
        ),
    ]
