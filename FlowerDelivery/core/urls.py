from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # Маршрут для регистрации
    path('', views.home, name='home'),  # Главная страница
]