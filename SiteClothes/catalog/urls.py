from django.urls import path
from . import views
from .views import (
    apply_promocode,
)

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.News, name='news'),
    path('contacts/', views.Contacts, name='contacts'),
    path('cart/', views.view_cart, name='view_cart'),
    path('products/', views.product_list, name='view_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/item/<int:item_id>/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('plus/<int:item_id>/', views.plus_from_cart, name='plus_from_cart'),
    path('minus/<int:item_id>/', views.minus_from_cart, name='minus_from_cart'),
    path('apply-promocode/', apply_promocode, name='apply_promocode'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('favorites/add/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/get-ids/', views.get_favorite_ids, name='get_favorite_ids'),
    path('order/create/', views.create_order, name='create_order'),
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]

