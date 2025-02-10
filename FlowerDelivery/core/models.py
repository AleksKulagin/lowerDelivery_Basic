from django.db import models

class User(models.Model):
    """
    Модель для хранения информации о пользователях.
    """
    name = models.CharField(unique=True, max_length=100, verbose_name="Имя пользователя")
    email = models.EmailField(unique=True, verbose_name="Электронная почта")

    def __str__(self):
        return self.name

class Product(models.Model):
    """
    Модель для хранения информации о товарах (цветах).
    """
    name = models.CharField(max_length=100, verbose_name="Название товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение товара", null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.price} руб."

class Order(models.Model):
    """
    Модель для хранения информации о заказах.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    products = models.ManyToManyField(Product, verbose_name="Товары")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.name}"