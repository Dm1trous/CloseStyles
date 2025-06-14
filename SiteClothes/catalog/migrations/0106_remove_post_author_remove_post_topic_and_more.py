# Generated by Django 5.2.1 on 2025-06-08 08:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0105_alter_cartitem_options_stock_clothes_available_sizes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.RemoveField(
            model_name='post',
            name='topic',
        ),
        migrations.AlterModelOptions(
            name='brend',
            options={'verbose_name': 'Бренд', 'verbose_name_plural': 'Бренды'},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'Товар в корзине', 'verbose_name_plural': 'Товары в корзине'},
        ),
        migrations.AlterModelOptions(
            name='cat',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='clothes',
            options={'ordering': ['-dates'], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AlterModelOptions(
            name='color',
            options={'verbose_name': 'Цвет', 'verbose_name_plural': 'Цвета'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'Страна', 'verbose_name_plural': 'Страны'},
        ),
        migrations.AlterModelOptions(
            name='gender',
            options={'verbose_name': 'Пол', 'verbose_name_plural': 'Пол'},
        ),
        migrations.AlterModelOptions(
            name='material',
            options={'verbose_name': 'Материал', 'verbose_name_plural': 'Материалы'},
        ),
        migrations.AlterModelOptions(
            name='newss',
            options={'ordering': ['-dates'], 'verbose_name': 'Новость', 'verbose_name_plural': 'Новости'},
        ),
        migrations.AlterModelOptions(
            name='size',
            options={'verbose_name': 'Размер', 'verbose_name_plural': 'Размеры'},
        ),
        migrations.RemoveField(
            model_name='clothes',
            name='available_sizes',
        ),
        migrations.RemoveField(
            model_name='clothes',
            name='sizee',
        ),
        migrations.AddField(
            model_name='clothes',
            name='old_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Старая цена'),
        ),
        migrations.AlterField(
            model_name='brend',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Бренд'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.size', verbose_name='Размер'),
        ),
        migrations.AlterField(
            model_name='cat',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='brendd',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.brend', verbose_name='Бренд'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='catt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.cat', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='colorr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.color', verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='countryy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='catalog.country', verbose_name='Страна производитель'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='dates',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='genderr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.gender', verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='imgg',
            field=models.ImageField(upload_to='products/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='statuss',
            field=models.BooleanField(default=True, verbose_name='Активен (в продаже)'),
        ),
        migrations.AlterField(
            model_name='clothes',
            name='summ',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость'),
        ),
        migrations.AlterField(
            model_name='color',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Страна'),
        ),
        migrations.AlterField(
            model_name='gender',
            name='name',
            field=models.CharField(max_length=20, unique=True, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='material',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Материал'),
        ),
        migrations.AlterField(
            model_name='newss',
            name='dates',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='newss',
            name='img',
            field=models.ImageField(upload_to='news/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='newss',
            name='text',
            field=models.TextField(verbose_name='Текст статьи'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Итоговая стоимость'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена за единицу'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.size', verbose_name='Размер'),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Активен'),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='discount_percentage',
            field=models.PositiveIntegerField(default=0, verbose_name='Процент скидки'),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='max_discount_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Максимальная сумма скидки'),
        ),
        migrations.AlterField(
            model_name='size',
            name='name',
            field=models.CharField(max_length=20, unique=True, verbose_name='Размер'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_set', to='catalog.clothes', verbose_name='Товар'),
        ),
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('user', 'product', 'size')},
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
    ]
