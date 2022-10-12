# Generated by Django 4.1.1 on 2022-09-05 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mebel_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={},
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название товара')),
                ('color', models.CharField(max_length=50, verbose_name='Цвет')),
                ('price', models.FloatField(max_length=20, verbose_name='Цена')),
                ('description', models.TextField(verbose_name='Описание товара')),
                ('quantity', models.IntegerField(verbose_name='Кол-во на складе')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='mebel_app.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='product/', verbose_name='Изображения')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mebel_app.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Галерея товаров',
            },
        ),
    ]
