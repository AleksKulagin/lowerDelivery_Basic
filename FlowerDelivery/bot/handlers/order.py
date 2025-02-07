from telegram import Update
from telegram.ext import ContextTypes

try:
    from core.models import Order
    print("Импорт модели Order выполнен успешно!")
except ImportError as e:
    print(f"Ошибка импорта модели Order: {e}")


async def order_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /orders. Отправляет список заказов.
    """
    orders = Order.objects.all()  # Получаем все заказы из базы данных
    if orders:
        for order in orders:
            message = (
                f"Заказ #{order.id}\n"
                f"Пользователь: {order.user.name}\n"
                f"Товары: {', '.join([product.name for product in order.products.all()])}\n"
                f"Дата: {order.created_at}"
            )
            await update.message.reply_text(message)
    else:
        await update.message.reply_text("Заказов пока нет.")

# Регистрируем обработчик команды /orders
order_handler = CommandHandler('orders', order_command)