from django.db.models.signals import post_save
from django.dispatch import receiver
from FlowerDelivery.core.models import Order
from FlowerDelivery.bot.bot import BOT_TOKEN
from telegram import Bot

@receiver(post_save, sender=Order)
def notify_new_order(sender, instance, created, **kwargs):
    """
    Сигнал для отправки уведомления о новом заказе.
    """
    if created:
        bot = Bot(token=BOT_TOKEN)
        message = (
            f"Новый заказ!\n"
            f"Заказ #{instance.id}\n"
            f"Пользователь: {instance.user.name}\n"
            f"Товары: {', '.join([product.name for product in instance.products.all()])}\n"
            f"Дата: {instance.created_at}"
        )
        bot.send_message(chat_id="YOUR_CHAT_ID", text=message)  # Замените на ваш chat_id