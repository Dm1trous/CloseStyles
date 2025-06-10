from django.db import transaction
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models import Count, OuterRef, Subquery
from django.core.paginator import Paginator
from django.db.models import Q

from .models import (clothes, newss, CartItem, size, color,
                     brend, gender, cat, material, PromoCode, Favorite, Order,
                     OrderItem, Stock)


# Для получения количества товаров в корзине
def get_cart_quantity(user):
    if user.is_authenticated:
        return sum(item.quantity for item in CartItem.objects.filter(user=user))
    return 0

# Для получения количества товаров в избранном
def get_favorites_quantity(user):
    if user.is_authenticated:
        return Favorite.objects.filter(user=user).count()
    return 0


# Главная страница
def index(request):
    gender_filter = request.GET.get("gender", "all")
    if gender_filter == "male":
        latest_products = clothes.in_stock.filter(genderr__name="Мужчины").order_by("-dates")[:5]
    elif gender_filter == "female":
        latest_products = clothes.in_stock.filter(genderr__name="Женщины").order_by("-dates")[:5]
    else:
        latest_products = clothes.in_stock.order_by("-dates")[:5]

    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)

    context = {
        'latest_products': latest_products,
        'favorite_ids': list(favorite_ids),
        'num_clothes': len(latest_products),
        'total_quantity': get_cart_quantity(request.user),
        'favorites_quantity': get_favorites_quantity(request.user)
    }
    return render(request, 'catalog/index.html', context)

# Страница "Контакты"
def Contacts(request):
    context = {
        'total_quantity': get_cart_quantity(request.user),
        'favorites_quantity': get_favorites_quantity(request.user)
    }
    return render(request, "catalog/contacts.html", context)

# Страница "Новости"
def News(request):
    news = newss.objects.order_by('-dates')
    context = {
        'news': news,
        'total_quantity': get_cart_quantity(request.user),
        'favorites_quantity': get_favorites_quantity(request.user)
    }
    return render(request, "catalog/news.html", context)

# Карточка товара
def product_detail(request, product_id):
    product = get_object_or_404(clothes, id=product_id)
    product_in_favorites = False
    if request.user.is_authenticated:
        product_in_favorites = Favorite.objects.filter(user=request.user, product=product).exists()

    context = {
        'product': product,
        'product_in_favorites': product_in_favorites,
        'total_quantity': get_cart_quantity(request.user),
        'favorites_quantity': get_favorites_quantity(request.user)
    }
    return render(request, 'catalog/product_detail.html', context)

# Корзина
def view_cart(request):
    if request.user.is_authenticated:
        stock_quantity_subquery = Stock.objects.filter(
            product=OuterRef('product_id'),
            size=OuterRef('size_id')
        ).values('quantity')[:1]

        cart_items = CartItem.objects.filter(user=request.user).annotate(
            stock_quantity=Coalesce(Subquery(stock_quantity_subquery), 0)
        ).select_related('product', 'size', 'product__colorr').order_by("-date_added")

        total_price = sum(item.product.summ * item.quantity for item in cart_items)
        applied_discount = 0
        applied_promocode = None

        if 'applied_promocode' in request.session:
            try:
                promo_code = PromoCode.objects.get(code=request.session['applied_promocode'], active=True)
                calculated_discount = total_price * promo_code.discount_percentage // 100
                applied_discount = min(calculated_discount,
                                    promo_code.max_discount_amount) if promo_code.max_discount_amount else calculated_discount
                applied_promocode = promo_code
            except PromoCode.DoesNotExist:
                if 'applied_promocode' in request.session:
                    del request.session['applied_promocode']

        final_total = total_price - applied_discount

        favorite_ids = list(Favorite.objects.filter(user=request.user).values_list('product_id', flat=True))

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
            'final_total': final_total,
            'discount_amount': applied_discount,
            'total_quantity': get_cart_quantity(request.user),
            'favorite_ids': favorite_ids,
            'favorites_quantity': get_favorites_quantity(request.user),
            'applied_promocode': applied_promocode
        }
    else:
        context = {
            'total_quantity': 0,
            'cart_items': []
        }
    return render(request, 'catalog/cart.html', context)

# Добавление в корзину
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Требуется авторизация'}, status=403)

    product = get_object_or_404(clothes, id=product_id)
    size_id = request.GET.get('size_id')

    if not size_id:
        return JsonResponse({'status': 'error', 'message': 'Размер не выбран'}, status=400)

    try:
        stock_item = Stock.objects.get(product=product, size__id=int(size_id))
    except (Stock.DoesNotExist, ValueError):
        return JsonResponse({'status': 'error', 'message': 'Неверный размер'}, status=400)

    chosen_size = stock_item.size

    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        user=request.user,
        size=chosen_size,
        defaults={'quantity': 0}
    )

    if stock_item.quantity > cart_item.quantity:
        cart_item.quantity += 1
        cart_item.save()
        status = 'success'
        message = 'Товар добавлен в корзину'
    else:
        status = 'error'
        message = f'Нельзя добавить больше. На складе всего {stock_item.quantity} шт.'

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': status,
            'message': message,
            'total_quantity': get_cart_quantity(request.user),
        })

    return redirect('catalog:view_cart')

# Удаление из корзины
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('catalog:view_cart')

# Увеличение количества товара в корзине на 1
def plus_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)

    try:
        stock_item = Stock.objects.get(product=cart_item.product, size=cart_item.size)

        if stock_item.quantity > cart_item.quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            pass
    except Stock.DoesNotExist:
        pass

    return redirect('catalog:view_cart')

# Уменьшение количества товара в корзине на 1
def minus_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.quantity -= 1
    if cart_item.quantity < 1:
        cart_item.delete()
    else:
        cart_item.save()
    return redirect('catalog:view_cart')

# Применение промокода
def apply_promocode(request):
    if request.method == 'POST':
        promocode_value = request.POST.get('promocode')
        try:
            promo_code = PromoCode.objects.get(code=promocode_value, active=True)
            cart_items = CartItem.objects.filter(user=request.user)
            total_price = sum(item.product.summ * item.quantity for item in cart_items)
            calculated_discount = total_price * promo_code.discount_percentage / 100
            if promo_code.max_discount_amount and calculated_discount > promo_code.max_discount_amount:
                calculated_discount = promo_code.max_discount_amount
            final_total = total_price - calculated_discount
            request.session['applied_promocode'] = promocode_value
            request.session.modified = True

            return JsonResponse({
                'success': True,
                'message': 'Промокод успешно применен',
                'discount_amount': int(calculated_discount),
                'final_total': int(final_total),
                'promocode_code': promo_code.code,
                'discount_percentage': promo_code.discount_percentage
            })
        except PromoCode.DoesNotExist:
            if 'applied_promocode' in request.session:
                del request.session['applied_promocode']
            return JsonResponse({'success': False, 'message': 'Промокод не найден'}, status=400)
    return JsonResponse({'success': False, 'message': 'Неверный запрос'}, status=400)

# Удаление промокода
def remove_promocode(request):
    if 'applied_promocode' in request.session:
        del request.session['applied_promocode']
        request.session.modified = True
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.summ * item.quantity for item in cart_items)
    return JsonResponse({'success': True, 'discount_amount': 0, 'final_total': total_price})

# Каталог с фильтрацией сортировкой и пагинацией
def product_list(request):
    search_query = request.GET.get('q', '')
    sort_order = request.GET.get('sort', '')
    size_ids = request.GET.getlist('size')
    color_ids = request.GET.getlist('color')
    brand_ids = request.GET.getlist('brand')
    gender_id = request.GET.get('gender')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category_ids = request.GET.getlist('category')
    material_ids = request.GET.getlist('material')

    products_qs = clothes.objects.all().order_by('-dates')

    if search_query:
        products_qs = products_qs.filter(Q(title__icontains=search_query) | Q(brendd__name__icontains=search_query))
    if size_ids:
        products_qs = products_qs.filter(available_sizes__in=size_ids).distinct()
    if color_ids:
        products_qs = products_qs.filter(colorr__in=color_ids)
    if brand_ids:
        products_qs = products_qs.filter(brendd__in=brand_ids)
    if gender_id and gender_id != 'all':
        products_qs = products_qs.filter(genderr__id=gender_id)
    if category_ids:
        products_qs = products_qs.filter(catt__in=category_ids)
    if material_ids:
        products_qs = products_qs.filter(materiall__in=material_ids)
    if min_price and max_price and min_price.isdigit() and max_price.isdigit():
        products_qs = products_qs.filter(summ__gte=min_price, summ__lte=max_price)

    if sort_order == 'name_asc':
        products_qs = products_qs.order_by('title')
    elif sort_order == 'name_desc':
        products_qs = products_qs.order_by('-title')
    elif sort_order == 'price_asc':
        products_qs = products_qs.order_by('summ')
    elif sort_order == 'price_desc':
        products_qs = products_qs.order_by('-summ')

    all_filtered_products = list(products_qs.prefetch_related('stock_set'))

    products_in_stock_list = [p for p in all_filtered_products if p.is_in_stock]

    genders = gender.objects.annotate(product_count=Count('clothes'))
    sizes = size.objects.annotate(product_count=Count('stock', distinct=True)).distinct()
    brands = brend.objects.annotate(product_count=Count('clothes', distinct=True)).distinct()
    categories = cat.objects.annotate(product_count=Count('clothes', distinct=True)).distinct()
    materials = material.objects.all()

    paginator = Paginator(products_in_stock_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = list(Favorite.objects.filter(user=request.user).values_list('product_id', flat=True))

    context = {
        'page_obj': page_obj,
        'sizes': sizes,
        'colors': color.objects.all(),
        'brands': brands,
        'genders': genders,
        'categories': categories,
        'materials': materials,
        'selected_genders': gender_id,
        'selected_colors': color_ids,
        'selected_brands': brand_ids,
        'selected_sizes': size_ids,
        'selected_categories': category_ids,
        'selected_materials': material_ids,
        'min_price': min_price,
        'max_price': max_price,
        'sort_order': sort_order,
        'all_products_count': clothes.objects.count(),
        'total_quantity': get_cart_quantity(request.user),
        'favorite_ids': favorite_ids,
        'favorites_quantity': get_favorites_quantity(request.user)
    }
    return render(request, 'catalog/products.html', context)

# Избранное
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product').order_by("-date_added")
    context = {
        'favorites': favorites,
        'total_quantity': get_cart_quantity(request.user),
        'favorites_quantity': get_favorites_quantity(request.user)
    }
    return render(request, 'catalog/favorites.html', context)

# Добавление в избранное
def add_to_favorites(request, product_id):
    product = get_object_or_404(clothes.objects, id=product_id)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        product=product
    )
    return JsonResponse({
        'success': True,
        'is_added': created,
        'product_title': product.title,
        'favorites_count': Favorite.objects.filter(user=request.user).count()
    })

# Удаление из избранного
def remove_from_favorites(request, product_id):
    favorite = get_object_or_404(Favorite, user=request.user, product_id=product_id)
    product_title = favorite.product.title
    favorite.delete()
    return JsonResponse({
        'success': True,
        'product_title': product_title,
        'favorites_count': Favorite.objects.filter(user=request.user).count()
    })

# Получение всех товаров в избранном
def get_favorite_ids(request):
    favorite_ids = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
    return JsonResponse({'favorite_ids': list(favorite_ids)})

# Создание заказа из корзины
def create_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return redirect('catalog:view_cart')

    for item in cart_items:
        if not item.product.statuss or not item.is_size_available:
            return redirect('catalog:view_cart')

    with transaction.atomic():
        total_price = sum(item.product.summ * item.quantity for item in cart_items)
        applied_promocode = None
        applied_discount = 0

        if 'applied_promocode' in request.session:
            try:
                promo = PromoCode.objects.get(code=request.session['applied_promocode'], active=True)
                calculated_discount = total_price * promo.discount_percentage // 100
                if promo.max_discount_amount:
                    applied_discount = min(calculated_discount, promo.max_discount_amount)
                else:
                    applied_discount = calculated_discount
                applied_promocode = promo
            except PromoCode.DoesNotExist:
                del request.session['applied_promocode']

        final_total = total_price - applied_discount
        order = Order.objects.create(
            user=request.user,
            total_price=final_total,
            promocode=applied_promocode
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                size=item.size.name,
                price=item.product.summ,
                quantity=item.quantity
            )
            try:
                stock_item = Stock.objects.select_for_update().get(product=item.product, size=item.size)

                if stock_item.quantity >= item.quantity:
                    stock_item.quantity -= item.quantity
                    stock_item.save()
                else:
                    raise Exception(f"Недостаточно товара {item.product.title} размера {item.size.name} на складе.")
            except Stock.DoesNotExist:
                raise Exception(f"Товар {item.product.title} размера {item.size.name} не найден на складе.")

            cart_items.delete()

        cart_items.delete()
        if 'applied_promocode' in request.session:
            del request.session['applied_promocode']

    request.session['order_success_message'] = f"Заказ (самовывоз) успешно оформлен!"
    return redirect('catalog:order_detail', order_id=order.id)

# Отображение списка заказов
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
        'total_quantity': get_cart_quantity(request.user),
        'favorites_quantity': get_favorites_quantity(request.user)
    }
    return render(request, 'catalog/order_list.html', context)


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()
    order_success_message = request.session.pop('order_success_message', None)
    subtotal = sum(item.get_cost() for item in order_items)
    discount_amount = 0
    if order.promocode:
        discount_amount = subtotal - order.total_price

    total_order_quantity = sum(item.quantity for item in order_items)

    context = {
        'order': order,
        'order_items': order_items,
        'subtotal': subtotal,
        'discount_amount': discount_amount,
        'final_total': order.total_price,
        'total_order_quantity': total_order_quantity,
        'order_success_message': order_success_message,
        'total_quantity': get_cart_quantity(request.user),
        'favorites_quantity': get_favorites_quantity(request.user)
    }
    return render(request, 'catalog/order_detail.html', context)
