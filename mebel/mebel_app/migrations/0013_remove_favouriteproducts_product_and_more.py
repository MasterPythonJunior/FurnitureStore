# Generated by Django 4.1.2 on 2022-10-07 06:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mebel_app', '0012_customer_order_orderproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favouriteproducts',
            name='product',
        ),
        migrations.AlterField(
            model_name='favouriteproducts',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
        migrations.AddField(
            model_name='favouriteproducts',
            name='product',
            field=models.ManyToManyField(blank=True, null=True, to='mebel_app.product', verbose_name='продукты'),
        ),
    ]
