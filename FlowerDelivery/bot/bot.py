from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from asgiref.sync import sync_to_async
import os
import sys
import logging

# Добавляем путь к проекту в PYTHONPATH
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

# Настройка Django для работы вне основного приложения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FlowerDelivery.settings')

import django
django.setup()

try:
    from core.models import Order

except ImportError as e:
    print(f"Ошибка импорта модели Order: {e}")

from config import BOT_TOKEN

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

@dp.message(Command("start"))
async def start_handler(message: Message):
    """
    Обработчик команды /start.
    """
    await message.answer("Добро пожаловать! Используйте /orders для получения списка заказов.")

@dp.message(Command("orders"))
async def get_orders_handler(message: Message):
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
            logger.info(f"Сообщение отправлено: {message_text}")
    else:
        await message.answer("Заказов пока нет.")
        logger.info("Сообщение отправлено: Заказов пока нет.")

async def main():
    """
    Запуск бота.
    """
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())