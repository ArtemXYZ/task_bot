"""
Все конфиги проекта
"""
# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------- Импорт стандартных библиотек Пайтона
import os
# ---------------------------------- Импорт сторонних библиотек
from dotenv import find_dotenv, load_dotenv  # Для переменных окружения
load_dotenv(find_dotenv())  # Загружаем переменную окружения
# ----------------------------------------------------------------------------------------------------------------------
BOT_TOKEN = os.getenv('BOT_TOKEN')

# ---------------------------- Конфигурации подключения к базам данных
CONFIG_SKY_NET_ASYNCPG = {
    'drivername': os.environ.get("DRIVERNAME_ASYNCPG"),
    'username': os.environ.get("USERNAME"),
    'password': os.environ.get("PASSWORD"),
    'host': os.environ.get("HOST"),
    'port': os.environ.get("PORT"),
    'database': os.environ.get("DATABASE")
}


ADMIN = os.environ.get("ADMIN_DEFAULT_TG_ID")
