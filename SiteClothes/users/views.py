from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User


from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm



def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            authenticate(username=form.cleaned_data['username'],
                         password=form.cleaned_data['password1'],
                        )
            auth_login(request, user)
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/registration.html', {'form': form})

def login(request):
    return render(request, 'users/login.html')

def profile(request, username=None):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        forma = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid() and forma.is_valid():
            form.save()
            forma.save()
            messages.success(request, f'Данные обновлены!')
            return redirect('profile', username=request.user.username)


        return redirect('profile', username=request.user.username)

    else:
        form = UserUpdateForm()
        forma = ProfileUpdateForm()
        context = {
            'form': form,
            'forma': forma,
        }

        if request.user.username == username:
            form = UserUpdateForm(instance=request.user)
            forma = ProfileUpdateForm(instance=request.user.profile)

            context['form'] = form
            context['forma'] = forma

        if username is not None:
            user = User.objects.get(username=username)
            context['user'] = user

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_quantity = sum(item.quantity for item in cart_items)
        context['total_quantity'] = total_quantity
        context['form'] = form
        context['forma'] = forma

        return render(request, "users/profile.html", context)

    return render(request, 'users/profile.html', context)
