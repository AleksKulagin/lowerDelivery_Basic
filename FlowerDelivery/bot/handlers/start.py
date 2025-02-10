from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message

async def start_command(message: Message):
    """
    Обработчик команды /start.
    """
    await message.answer("Добро пожаловать! Используйте /orders для получения списка заказов.")

# Регистрируем обработчик команды /start
start_handler = Command("start")(start_command)