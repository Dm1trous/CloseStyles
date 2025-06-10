from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse

from .models import (clothes, newss, CartItem, gender,
                     brend, size, cat, color, material, PromoCode, country,
                     Favorite, Order, OrderItem, Stock)

# Админка для ТОВАРОВ

class StockInline(admin.TabularInline):
    model = Stock
    extra = 1
    autocomplete_fields = ['size']

@admin.register(clothes)
class ClothesAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_show', 'title', 'summ', 'catt', 'genderr', 'brendd', 'statuss')
    list_display_links = ('id', 'image_show', 'title')
    list_filter = ('statuss', 'genderr', 'catt', 'brendd')
    search_fields = ('title', 'description', 'brendd__name')
    list_editable = ('statuss', 'summ')
    fieldsets = (
        ('Основная информация', {'fields': ('title', 'description', 'summ', 'statuss')}),
        ('Описание', {'fields': ('catt', 'genderr', 'brendd', 'countryy')}),
        ('Характеристики', {'fields': ('materiall', 'colorr')}),
        ('Изображение', {'fields': ('imgg',)}),
    )
    inlines = [StockInline]
    autocomplete_fields = ['catt', 'genderr', 'brendd', 'countryy', 'colorr']
    filter_horizontal = ('materiall',)

    @admin.display(description="Фото")
    def image_show(self, obj):
        if obj.imgg:
            return mark_safe(f"<img src='{obj.imgg.url}' width='60' />")
        return "Нет фото"


# Админка для ЗАКАЗОВ

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    readonly_fields = ('get_cost',)

    @admin.display(description="Стоимость")
    def get_cost(self, obj):
        return obj.get_cost()

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_link', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'id')
    list_display_links = ('id', 'user_link')
    inlines = [OrderItemInline]
    readonly_fields = ('user', 'created_at', 'updated_at', 'total_price', 'promocode')

    @admin.display(description="Пользователь")
    def user_link(self, obj):
        link = reverse("admin:auth_user_change", args=[obj.user.id])
        return mark_safe(f'<a href="{link}">{obj.user.username}</a>')


# Админка для КОНТЕНТА (Новости и Форум)

@admin.register(newss)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'dates')
    search_fields = ('name', 'text')

    @admin.display(description="Текст комментария")
    def short_body(self, obj):
        return obj.body[:50] + '...' if len(obj.body) > 50 else obj.body


# Админка для ПРОМОКОДОВ и ПОЛЬЗОВАТЕЛЕЙ

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'max_discount_amount', 'active')
    list_editable = ('active', 'discount_percentage')
    search_fields = ('code',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'date_added')
    list_filter = ('user',)
    search_fields = ('user__username', 'product__title')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'size', 'quantity', 'date_added')
    list_filter = ('user',)
    search_fields = ('user__username', 'product__title')


# Остальные модели (скрыты)

class ReferenceAdmin(admin.ModelAdmin):
    search_fields = ('name',)

    def has_module_permission(self, request):
        return False

admin.site.register(brend, ReferenceAdmin)
admin.site.register(country, ReferenceAdmin)
admin.site.register(gender, ReferenceAdmin)
admin.site.register(cat, ReferenceAdmin)
admin.site.register(color, ReferenceAdmin)
admin.site.register(size, ReferenceAdmin)
admin.site.register(material, ReferenceAdmin)