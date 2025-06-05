from django.urls import path
from . import views
from .views import (
    TopicCreateView,
    TopicListView,
    TopicDetailView,
    PostCreateView,
    PostDetailView,
    PostDeleteView,
    apply_promocode,
)

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('forum/', TopicListView.as_view(), name='forum-index'),
    path('topic/add/', TopicCreateView.as_view(), name='topic-add'),
    path('topic/<int:pk>/', TopicDetailView.as_view(), name='topic-detail'),
    path('topic/<int:pk>/newpost/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('news/', views.News, name='news'),
    path('contacts/', views.Contacts, name='contacts'),
    path('cart/', views.view_cart, name='view_cart'),
    path('products/', views.product_list, name='view_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('plus/<int:item_id>/', views.plus_from_cart, name='plus_from_cart'),
    path('minus/<int:item_id>/', views.minus_from_cart, name='minus_from_cart'),
    path('apply-promocode/', apply_promocode, name='apply_promocode'),
]

