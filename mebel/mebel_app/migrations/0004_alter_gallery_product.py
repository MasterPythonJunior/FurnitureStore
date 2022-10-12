# Generated by Django 4.1.1 on 2022-09-10 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mebel_app', '0003_alter_category_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='mebel_app.product', verbose_name='Товар'),
        ),
    ]
