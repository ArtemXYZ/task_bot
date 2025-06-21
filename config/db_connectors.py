"""
    Модуль содержит функции асинхронного подключения к базам данных.
    Для асинхронного подключения обязательно использовать конфиг типа: CONFIG_RNAME=postgresql+asyncpg.
    Обязательна установка библиотеки asyncpg.
"""
# check_telegram_id
# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------- Импорт стандартных библиотек
# import logging
# import pprint
# ---------------------------------- Импорт сторонних библиотек
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

# -------------------------------- Локальные модули
from config.configs import *


# ======================================================================================================================
# Создаем URL строку: todo уточнить функцию и аннотации
def get_url_string(any_config: dict | URL | str) -> URL | dict | URL | str | None:
    """"
        Проверка типа входной конфигурации подключения:
        Если на вход конфигурация в словаре:
    """

    url_string: dict | URL | str | None = None

    if isinstance(any_config, dict):
        url_string = URL.create(**any_config)  # 1. Формируем URL-строку соединения с БД.

    # Если на вход url_conf_locdb:
    elif isinstance(any_config, str):
        url_string = any_config
    else:
        url_string = None

    return url_string


# ----------------------------------------------------------------------------------------------------------------------
# Синхронные подключения:
# url_string = get_url_string(CONFIG_SKY_NET_ASYNCPG)
# sinc_engine_mart_sv = create_engine(url_string)  # , echo=True

# ----------------------------------------------------------------------------------------------------------------------
#                                                           ***
# ----------------------------------------------------------------------------------------------------------------------
# Асинхронные подключения:

# ------------------------------------------- Создаем общую сессию с удаленными бд для всех модулей:
sky_conf = get_url_string(CONFIG_SKY_NET_ASYNCPG)
sky_engine = create_async_engine(sky_conf)  # , echo=True (Для логирования)!
SKY_SESSION = async_sessionmaker(bind=sky_engine, class_=AsyncSession, expire_on_commit=False)  # False


#  todo разобраться с функцией может оставить ее синхронной, уточнить аннотацию
async def get_rdb_session(session: AsyncSession = SKY_SESSION) -> AsyncSession:
    """
        Функция возвращает готовый объект сессии (AsyncSession) с удаленной базой данных.
        Предназначена для передачи как вложенной в другие функции, что позволит при необходимости менять сессию
        только в 1 месте.
    """
    return session()