import sys
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

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



from config import BOT_TOKEN  # Импортируем токен из config.py

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

def main():
    """
    Запуск бота.
    """
    # Создаем приложение и передаем токен бота
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("orders", get_orders))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()