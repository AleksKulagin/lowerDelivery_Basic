from telegram import Update
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start.
    """
    await update.message.reply_text("Добро пожаловать! Используйте /orders для получения списка заказов.")

# Регистрируем обработчик команды /start
start_handler = CommandHandler('start', start_command)