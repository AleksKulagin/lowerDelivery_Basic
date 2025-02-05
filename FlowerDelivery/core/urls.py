from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('register/', views.register, name='register'),  # Регистрация
    path('products/', views.product_list, name='product_list'),  # Каталог товаров
]