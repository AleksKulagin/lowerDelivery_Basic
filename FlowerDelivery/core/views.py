from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import Product
from .forms import OrderForm
from datetime import time, datetime



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


def create_order(request):
    """
    View для оформления заказа.
    """

    # Получаем текущее время
    current_time = datetime.now().time()
    start_time = datetime.strptime('08:00', '%H:%M').time()
    end_time = datetime.strptime('20:00', '%H:%M').time()

    # Проверяем, находится ли текущее время в пределах рабочего времени
    if not (start_time <= current_time <= end_time):
        return render(request, 'work_day.html')  # Перенаправляем на страницу "work_day.html"

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправляем на главную страницу после оформления заказа
    else:
        form = OrderForm()

    # Отладочный вывод
    products = form.fields['products'].queryset  # Получаем queryset товаров
    for product in products:
        print(f"Product: {product.name}, Image: {product.image}")

    return render(request, 'create_order.html', {'form': form, 'products': products})