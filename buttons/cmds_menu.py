"""
    Модуль содержит описание кнопок меню для всех типов чартов.
"""

from aiogram.types import BotCommand

commands_menu = [
    BotCommand(command='start', description='Начать работу с ботом / получить инструкции по работе с ботом'),
    BotCommand(command='show_tasks', description='Показывает список задач'),
    BotCommand(command='add_task', description='Добавить новую задачу'),
    BotCommand(command='delete_task', description='Удалить задачу по ID'),
]