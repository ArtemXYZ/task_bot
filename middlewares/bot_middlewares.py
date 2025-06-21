"""
    Модуль "ПРОМЕЖУТОЧНЫХ СЛОЕВ" содержит пользовательские классы необходимых в дальнейшем
    для работы с базами данных (SQL запросов).
    В основном с помощью ОРМ.
"""

# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------- Импорт стандартных библиотек Пайтона
# ---------------------------------- Импорт сторонних библиотек
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_connectors import get_ldb_session
# ----------------------------------------------------------------------------------------------------------------------
class DataBaseSession(BaseMiddleware):
    def __init__(self):  #
        pass
        # self.session_pool: AsyncSession = LOCDB_SESSION   #session_pool
    #         def __init__(self, session_pool: async_sessionmaker):  #
    #         self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:

        async with await get_ldb_session() as session:
            data['session'] = session  # Передаем в словарь переменную, которая будет доступна в хендлерах.
            return await handler(event, data)

