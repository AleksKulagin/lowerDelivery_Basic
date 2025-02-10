
import sys
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from asgiref.sync import sync_to_async

# Добавляем путь к проекту в PYTHONPATH
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

# Настройка Django для работы вне основного приложения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FlowerDelivery.settings')

import django
django.setup()

try:
    from core.models import Order
    print("Импорт модели Order выполнен успешно!")
except ImportError as e:
    print(f"Ошибка импорта модели Order: {e}")

from config import BOT_TOKEN

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start.
    """
    await update.message.reply_text("Добро пожаловать! Используйте /orders для получения списка заказов.")

async def get_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /orders. Отправляет список заказов.
    """
    logger.info("Обработчик get_orders вызван")

    # Используем sync_to_async для выполнения синхронного запроса к базе данных
    orders = await sync_to_async(lambda: list(Order.objects.all()))()
    count = len(orders)
    logger.info(f"Найдено заказов: {count}")

    if orders:
        for order in orders:
            products = await sync_to_async(lambda: list(order.products.all()))()
            product_names = ', '.join([product.name for product in products])
            message = (
                f"Заказ #{order.id}\n"
                f"Пользователь: {order.user.name}\n"
                f"Товары: {product_names}\n"
                f"Дата: {order.created_at}"
            )
            await update.message.reply_text(message)
            logger.info(f"Сообщение отправлено: {message}")
    else:
        await update.message.reply_text("Заказов пока нет.")
        logger.info("Сообщение отправлено: Заказов пока нет.")

def main():
    """
    Запуск бота.
    """
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("orders", get_orders))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()