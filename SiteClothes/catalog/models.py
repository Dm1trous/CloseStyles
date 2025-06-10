from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class InStockManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(statuss=True)

class Stock(models.Model):
    product = models.ForeignKey('clothes', on_delete=models.CASCADE, verbose_name="Товар")
    size = models.ForeignKey('size', on_delete=models.CASCADE, verbose_name="Размер")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество на складе")

    class Meta:
        verbose_name = "Складской остаток"
        verbose_name_plural = "Складские остатки"
        unique_together = ('product', 'size')

    def __str__(self):
        return f"{self.product.title} - Размер: {self.size.name} ({self.quantity} шт.)"

class clothes(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.CharField(max_length=2000, verbose_name="Описание", null=True, blank=True)
    summ = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость") # Изменено на DecimalField для точности
    old_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Старая цена", null=True, blank=True)
    catt = models.ForeignKey('cat', on_delete=models.CASCADE, verbose_name="Категория")
    genderr = models.ForeignKey('gender', on_delete=models.CASCADE, verbose_name="Для")
    sizee = models.ManyToManyField('size', verbose_name="Размер", related_name='size', blank=True)
    materiall = models.ManyToManyField('material', verbose_name="Материал")
    colorr = models.ForeignKey('color', on_delete=models.CASCADE, verbose_name="Цвет")
    brendd = models.ForeignKey('brend', on_delete=models.CASCADE, verbose_name="Бренд")
    countryy = models.ForeignKey('country', on_delete=models.CASCADE, verbose_name="Страна производитель", null=True, blank=True)
    statuss = models.BooleanField(default=True, verbose_name="В наличии")
    imgg = models.ImageField(verbose_name="Фото", upload_to='image/')
    dates = models.DateTimeField(auto_now=True)
    available_sizes = models.ManyToManyField('size', through='Stock', through_fields=('product', 'size'), verbose_name="Доступные размеры и их количество")

    objects = models.Manager()
    in_stock = InStockManager()

    def display_size(self):
        return ', '.join([sizee.name for sizee in self.sizee.all()])
    display_size.short_description = 'Размер'

    def display_material(self):
        return ', '.join([materiall.name for materiall in self.materiall.all()])
    display_material.short_description = 'материал'

    @property
    def is_in_stock(self):
        if not self.statuss:
            return False
        total_quantity = self.stock_set.aggregate(total=Sum('quantity'))['total']
        return total_quantity is not None and total_quantity > 0

    @property
    def discount_percent(self):
        if self.old_price and self.summ < self.old_price:
            return round((1 - self.summ / self.old_price) * 100)
        return 0

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
        verbose_name = 'Корзину'
        verbose_name_plural = 'Корзина'

    @property
    def is_size_available(self):
        if self.product and self.size:
            try:
                stock_item = Stock.objects.get(product=self.product, size=self.size)
                return stock_item.quantity >= self.quantity
            except Stock.DoesNotExist:
                return False
        return False

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(clothes, on_delete=models.CASCADE, verbose_name="Товар")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные товары'
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"

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

class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Собирается'),
        ('shipped', 'Готов к выдаче'),
        ('delivered', 'Выдан'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Итоговая стоимость")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing', verbose_name="Статус заказа")
    promocode = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Промокод")

    @property
    def total_items_quantity(self):
        return sum(item.quantity for item in self.items.all())

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ №{self.id} (самовывоз) от {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(clothes, on_delete=models.PROTECT, verbose_name="Товар")
    size = models.CharField(max_length=20, verbose_name="Размер")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'

    def __str__(self):
        return f'{self.product.title} ({self.size})'

    def get_cost(self):
        if self.price is not None and self.quantity is not None:
            return self.price * self.quantity
        return 0
