from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ApplyPromoCodeForm, CreateCommentForm
from .models import clothes, newss, CartItem, Post, Topic, Comment, size, color, brend, gender, cat, material, PromoCode
from django.views.generic import ListView, DetailView, CreateView, DeleteView


def get_cart_quantity(user):
    """Вспомогательная функция для получения количества товаров в корзине"""
    if user.is_authenticated:
        cart_items = CartItem.objects.filter(user=user)
        return sum(item.quantity for item in cart_items)
    return 0


def index(request):
    # Извлекаем фильтры
    gender_filter = request.GET.get("gender", "all")

    # Формируем список товаров согласно фильтру
    if gender_filter == "male":
        latest_products = clothes.objects.filter(genderr__name="Мужчины").order_by("-dates")[:5]
    elif gender_filter == "female":
        latest_products = clothes.objects.filter(genderr__name="Женщины").order_by("-dates")[:5]
    else:
        latest_products = clothes.objects.order_by("-dates")[:5]

    context = {
        'latest_products': latest_products,
        'num_clothes': len(latest_products),
        'total_quantity': get_cart_quantity(request.user)
    }
    return render(request, 'catalog/base.html', context)


def Contacts(request):
    context = {
        'total_quantity': get_cart_quantity(request.user)
    }
    return render(request, "catalog/contacts.html", context)


def News(request):
    news = newss.objects.order_by('-dates')
    context = {
        'news': news,
        'total_quantity': get_cart_quantity(request.user)
    }
    return render(request, "catalog/news.html", context)


def product_detail(request, product_id):
    product = get_object_or_404(clothes, id=product_id)
    available_sizes = product.sizee.all()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'product_id': product.id,
            'product_title': product.title
        })

    context = {
        'product': product,
        'sizes': available_sizes,
        'total_quantity': get_cart_quantity(request.user)
    }
    return render(request, 'catalog/product_detail.html', context)


def view_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user).order_by("-date_added")
        total_price = sum(item.product.summ * item.quantity for item in cart_items)
        applied_discount = 0

        if 'applied_promocode' in request.session:
            promo_code = PromoCode.objects.get(code=request.session['applied_promocode'], active=True)
            calculated_discount = total_price * promo_code.discount_percentage // 100
            applied_discount = min(calculated_discount,
                                   promo_code.max_discount_amount) if promo_code.max_discount_amount else calculated_discount

        final_total = total_price - applied_discount

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
            'final_total': final_total,
            'discount_amount': applied_discount,
            'total_quantity': get_cart_quantity(request.user)
        }
    else:
        context = {
            'total_quantity': 0
        }

    return render(request, 'catalog/cart.html', context)


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Требуется авторизация'}, status=403)

    product = clothes.objects.get(id=product_id)
    size_id = request.GET.get('size_id')

    if size_id is None or int(size_id) not in list(product.sizee.values_list('id', flat=True)):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Неверный размер'}, status=400)
        raise Exception("Нет такого размера!")

    chosen_size = size.objects.get(id=int(size_id))

    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        user=request.user,
        size=chosen_size
    )
    cart_item.quantity += 1
    cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'total_quantity': get_cart_quantity(request.user)
        })

    return redirect('catalog:view_cart')


def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('catalog:view_cart')


def plus_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('catalog:view_cart')


def minus_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.quantity -= 1
    if cart_item.quantity < 1:
        cart_item.delete()
    else:
        cart_item.save()
    return redirect('catalog:view_cart')


def apply_promocode(request):
    if request.method == 'POST':
        form = ApplyPromoCodeForm(request.POST)
        if form.is_valid():
            promocode_value = form.cleaned_data['promocode']
            try:
                promo_code = PromoCode.objects.get(code=promocode_value, active=True)
                request.session['applied_promocode'] = promocode_value
                return redirect('catalog:view_cart')
            except PromoCode.DoesNotExist:
                pass
    return redirect('catalog:view_cart')


def product_list(request):
    # Получаем параметры фильтрации и сортировки
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

    # Базовый набор товаров
    products = clothes.objects.all().order_by('-dates')

    # Общая статистика по количеству товаров для каждого пола
    genders = gender.objects.annotate(product_count=Count('clothes'))

    # Применяем фильтры
    if search_query:
        products = products.filter(Q(title__icontains=search_query) | Q(brendd__name__icontains=search_query))

    if size_ids:
        products = products.filter(sizee__in=size_ids)

    if color_ids:
        products = products.filter(colorr__in=color_ids)

    if brand_ids:
        products = products.filter(brendd__in=brand_ids)

    if gender_id and gender_id != 'all':
        products = products.filter(genderr__id=gender_id)

    if category_ids:
        products = products.filter(catt__in=category_ids)

    if material_ids:
        products = products.filter(materiall__in=material_ids)

    if min_price and max_price and min_price != 'all' and max_price != 'all':
        products = products.filter(summ__gte=min_price, summ__lte=max_price)

    # Сортировка
    if sort_order == 'name_asc':
        products = products.order_by('title')
    elif sort_order == 'name_desc':
        products = products.order_by('-title')
    elif sort_order == 'price_asc':
        products = products.filter(summ__isnull=False).order_by('summ')
    elif sort_order == 'price_desc':
        products = products.filter(summ__isnull=False).order_by('-summ')

    # Получаем данные для фильтров
    sizes = size.objects.annotate(product_count=Count('size', distinct=True)).distinct()
    brends = brend.objects.annotate(product_count=Count('clothes', distinct=True)).distinct()
    categories = cat.objects.annotate(product_count=Count('clothes', distinct=True)).distinct()
    materials = material.objects.all()

    # Пагинация
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Формирование контекста
    context = {
        'page_obj': page_obj,
        'products': products,
        'sizes': sizes,
        'colors': color.objects.all(),
        'brands': brends,
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
        'total_quantity': get_cart_quantity(request.user)
    }

    return render(request, 'catalog/products.html', context)


class TopicListView(ListView):
    model = Topic
    template_name = 'forum/index.html'
    context_object_name = 'topics'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_quantity'] = get_cart_quantity(self.request.user)
        return context


class TopicDetailView(DetailView):
    model = Topic

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(topic=self.kwargs.get('pk'))
        context['total_quantity'] = get_cart_quantity(self.request.user)
        return context


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    fields = ['title']

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_quantity'] = get_cart_quantity(self.request.user)
        return context


class PostDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Post
    form_class = CreateCommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.kwargs.get('pk'))
        context['form'] = CreateCommentForm(initial={'post': self.object, 'author': self.request.user})
        context['total_quantity'] = get_cart_quantity(self.request.user)
        return context

    def get_success_url(self):
        return reverse('catalog:post-detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.topic = Topic.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_quantity'] = get_cart_quantity(self.request.user)
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/forum/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_quantity'] = get_cart_quantity(self.request.user)
        return context