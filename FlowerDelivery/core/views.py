from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import Product

def home(request):
    """
    View для главной страницы.
    """
    return render(request, 'home.html')

def register(request):
    """
    View для регистрации новых пользователей.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def product_list(request):
    """
    View для отображения каталога товаров.
    """
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})