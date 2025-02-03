from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

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
        # Если форма была отправлена, создаем форму с данными из запроса
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Сохраняем пользователя в базе данных
            form.save()
            # Перенаправляем пользователя на главную страницу
            return redirect('home')
    else:
        # Если запрос GET, создаем пустую форму
        form = UserRegistrationForm()

    # Отображаем форму регистрации
    return render(request, 'register.html', {'form': form})