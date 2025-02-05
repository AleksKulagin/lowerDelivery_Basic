from django import forms
from .models import User
from .models import Order, Product

class UserRegistrationForm(forms.ModelForm):
    """
    Форма для регистрации новых пользователей.
    """
    class Meta:
        model = User
        fields = ['name', 'email']  # Поля, которые будут отображаться в форме


class OrderForm(forms.ModelForm):
    """
    Форма для оформления заказа.
    """
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Используем чекбоксы для выбора товаров
        label="Выберите товары"
    )

    class Meta:
        model = Order
        fields = ['user', 'products']  # Поля, которые будут отображаться в форме