from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message
from asgiref.sync import sync_to_async

try:
    from core.models import Order
    print("Импорт модели Order выполнен успешно!")
except ImportError as e:
    print(f"Ошибка импорта модели Order: {e}")

async def order_command(message: Message):
    """
    Обработчик команды /orders. Отправляет список заказов.
    """
    # Используем sync_to_async для выполнения синхронного запроса к базе данных
    orders = await sync_to_async(lambda: list(Order.objects.all()))()

    if orders:
        for order in orders:
            # Используем sync_to_async для получения связанных объектов
            user = await sync_to_async(lambda: order.user)()
            products = await sync_to_async(lambda: list(order.products.all()))()
            product_names = ', '.join([product.name for product in products])
            message_text = (
                f"Заказ #{order.id}\n"
                f"Пользователь: {user.name}\n"
                f"Товары: {product_names}\n"
                f"Дата: {order.created_at}"
            )
            await message.answer(message_text)
    else:
        await message.answer("Заказов пока нет.")