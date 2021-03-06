# Generated by Django 2.2 on 2020-09-20 08:56

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Товар в заказе',
                'verbose_name_plural': 'Товары в заказе',
            },
        ),
        migrations.AlterModelOptions(
            name='basket',
            options={'verbose_name': 'Товар в корзине', 'verbose_name_plural': 'Товары в корзине'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterField(
            model_name='basket',
            name='amount',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Остаток'),
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(related_name='order_product', through='webapp.OrderProduct', to='webapp.Product', verbose_name='Продукты'),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='webapp.Order', verbose_name='Заказ'),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='webapp.Product', verbose_name='Товар'),
        ),
    ]
