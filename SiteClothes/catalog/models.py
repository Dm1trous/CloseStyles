from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import localtime


class clothes(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.CharField(max_length=2000, verbose_name="Описание", null=True, blank=True)
    summ = models.IntegerField(verbose_name="Стоимость")
    catt = models.ForeignKey('cat', on_delete=models.CASCADE, verbose_name="Категория")
    genderr = models.ForeignKey('gender', on_delete=models.CASCADE, verbose_name="Для")
    sizee = models.ManyToManyField('size', verbose_name="Размер", related_name='size')
    materiall = models.ManyToManyField('material', verbose_name="Материал")
    colorr = models.ForeignKey('color', on_delete=models.CASCADE, verbose_name="Цвет")
    brendd = models.ForeignKey('brend', on_delete=models.CASCADE, verbose_name="Бренд")
    countryy = models.ForeignKey('country', on_delete=models.CASCADE, verbose_name="Страна производитель", null=True)
    statuss = models.BooleanField(default=True, verbose_name="В наличии")
    imgg = models.ImageField(verbose_name="Фото", upload_to='image/')
    dates = models.DateTimeField(auto_now=True)


    def display_size(self):
        return ', '.join([sizee.name for sizee in self.sizee.all()])
    display_size.short_description = 'Размер'

    def display_material(self):
        return ', '.join([materiall.name for materiall in self.materiall.all()])
    display_material.short_description = 'материал'

    class Meta:
        verbose_name = 'Одежду'
        verbose_name_plural = 'Вся одежда'

    def __str__(self):
        return self.title

class brend(models.Model):
    name = models.CharField(max_length=50, verbose_name="Бренд")
    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Список брендов'
    def __str__(self):
        return self.name

class country(models.Model):
    name = models.CharField(max_length=50, verbose_name="Страна производитель")
    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Список стран'
    def __str__(self):
        return self.name

class gender(models.Model):
    name = models.CharField(max_length=20, verbose_name="Для кого")
    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Для кого'
    def __str__(self):
        return self.name

class size(models.Model):
    name = models.CharField(max_length=20, verbose_name="Введите размер")
    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Все размеры'
    def __str__(self):
        return self.name

class cat(models.Model):
    name = models.CharField(max_length=50, verbose_name="Категория")
    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
    def __str__(self):
        return self.name

class color(models.Model):
    name = models.CharField(max_length=50, verbose_name="Цвет")
    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвет'
    def __str__(self):
        return self.name

class material(models.Model):
    name = models.CharField(max_length=50, verbose_name="Материал")
    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материал'
    def __str__(self):
        return self.name

class newss(models.Model):
    name = models.CharField(max_length=200, verbose_name="Заголовок")
    text = models.TextField(max_length=5000, verbose_name="Текст статьи")
    img = models.ImageField(verbose_name="Фото", upload_to='image/', help_text="Рекомендуется изображение формата 1x1")
    dates = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Статью'
        verbose_name_plural = 'Статья'
    def __str__(self):
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey(clothes, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    size = models.ForeignKey(size, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Размер")
    date_added = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    def __str__(self):
        return f'{self.quantity} x {self.product.title}'


class Topic(models.Model):
    title = models.CharField(max_length=50, verbose_name="Заголовок")

    def get_absolute_url(self):
        return reverse('catalog:topic-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Заголовок категории форума'
        verbose_name_plural = 'Заголовок категории форума'

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, verbose_name="Заголовок")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Время")
    title = models.CharField(max_length=50, verbose_name="Заголовок поста")
    body = models.TextField(blank=True, null=True, verbose_name="Текст поста")

    class Meta:
        verbose_name = 'Пост пользователя'
        verbose_name_plural = 'Пост пользователя'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog:post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, verbose_name="Пост")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Время")
    body = models.TextField(verbose_name="Сообщение")

    class Meta:
        verbose_name = 'Коментарии под посты'
        verbose_name_plural = 'Коментарии под посты'

    def __str__(self):
        return self.body

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Код")
    discount_percentage = models.IntegerField(default=0, verbose_name="Процент скидки")
    max_discount_amount = models.IntegerField(default=None, null=True, blank=True, verbose_name="Максимальная сумма скидки")
    active = models.BooleanField(default=True, verbose_name="Активность")

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return self.code