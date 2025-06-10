from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from catalog.views import get_cart_quantity, get_favorites_quantity
from django.db.models import Sum, Count


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_own_profile = (request.user == profile_user)
    completed_orders = profile_user.order_set.filter(status='delivered')
    completed_orders_count = completed_orders.count()
    total_spent_data = completed_orders.aggregate(total_sum=Sum('total_price'))
    total_spent = total_spent_data['total_sum'] or 0

    context = {
        'profile_user': profile_user,
        'is_own_profile': is_own_profile,
        'completed_orders_count': completed_orders_count,
        'total_spent': total_spent,

        'total_quantity': get_cart_quantity(request.user),
        'favorites_quantity': get_favorites_quantity(request.user)
    }
    return render(request, 'users/profile_view.html', context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_view', username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Редактирование профиля',
        'total_quantity': get_cart_quantity(request.user),
        'favorites_quantity': get_favorites_quantity(request.user)
    }
    return render(request, 'users/profile_edit.html', context)