from django import forms
from .models import User

class UserRegistrationForm(forms.ModelForm):
    """
    Форма для регистрации новых пользователей.
    """
    class Meta:
        model = User
        fields = ['name', 'email']  # Поля, которые будут отображаться в форме