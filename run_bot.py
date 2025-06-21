"""
    Главный исполнительный файл, в котором осуществляется запуск и настройка телеграмм-бота,
    а также всех остальных модулей.
"""

# -------------------------------- Стандартные библиотеки
# import os
import asyncio
# import logging
# logging.basicConfig(level=logging.INFO)
# -------------------------------- Сторонние библиотеки
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeDefault
from aiogram.client.default import DefaultBotProperties  # Обработка текста HTML разметкой

# -------------------------------- Локальные модули
# from middlewares.bot_middlewares import TypeSessionMiddleware, DataBaseSession
from handlers.user_session import main_router
from buttons.cmds_menu import commands_menu  # Кнопки меню для всех типов чартов
from config.configs import BOT_TOKEN
from config.code_printer import *
# from services.start_sleep_bot import startup_service_db  # bot_shutdown,  bot_startup -
from handlers.user_session import *


# ----------------------------------------------------------------------------------------------------------------------
init_bot: Bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
# --------------------------------------------- Инициализация диспетчера событий:
init_dp = Dispatcher()

# Назначаем роутеры:
init_dp.include_router(main_router)


# -------------------------------------------------------------------------- bot_startup
async def bot_startup():  # bot: Bot=init_bot
    """
        Общая (основная) функция при запуске бота выполняет ряд программ для обеспечения нормальной работы бота.
    """

    # Удаление Webhook и всех ожидающих обновлений
    await init_bot.delete_webhook(drop_pending_updates=True)

    print(
        BACK_GREEN + BRIGHT_STYLE +
        f'                                                   * Запуск TASK BOT *'
        f'                                                    ')

    print(
        BACK_WHITE + BRIGHT_STYLE + LIGHTBLACK +
        '==========================================================='
        '===========================================================')

    print(BLUE + BRIGHT_STYLE + 'Запуск сервисных программ:')
    print(GREEN + "< Webhook удален и ожидающие обновления сброшены.")
    print(BACK_CYAN + LIGHTBLACK + 'Бот запущен, все норм!')

# -------------------------------------------------------------------------- bot_shutdown
async def bot_shutdown(init_bot=init_bot):  # ! Ошибка ожидает init_bot
    """
        Корректное завершение работы вашего бота (stop_polling).
        Вызовите метод stop_polling: Если вы используете метод длительного опроса (start_polling)
        для получения обновлений от серверов Telegram, убедитесь, что вы вызываете метод stop_polling
        при завершении работы вашего бота. Это позволит корректно завершить процесс опроса серверов Telegram.
    """

    # Останавливаем процесс получения обновлений:
    await init_dp.stop_polling()
    await asyncio.sleep(1)
    # Закрытие сессии бота при завершении работы:
    await init_bot.close()

    print(BACK_GREEN + RED + BRIGHT_STYLE + 'Бот остановлен!')


# --------------------------------------------------------------------------
# ---------------------------------------------------- Зацикливание работы бота
# Отслеживание событий на сервере тг бота:
async def run_bot():
    init_dp.startup.register(bot_startup)  # действия при старте бота +
    init_dp.shutdown.register(bot_shutdown)  # действия при остановке бота +

    # Установка промежуточного слоя (сразу для диспетчера, не для роутеров):
    # init_dp.update.middleware(DataBaseSession())  # ! Сейчас не требуется.

    # Сброс отправленных сообщений, за время, что бот был офлайн.
    await init_bot.delete_webhook(drop_pending_updates=True)

    # Если надо удалить команды из меню.
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())

    # Список команд в меню:
    await init_bot.set_my_commands(commands=commands_menu, scope=BotCommandScopeDefault())

    await init_dp.start_polling(
        init_bot,
        skip_updates=True,
        polling_timeout=2,
        handle_signals=True,
        close_bot_session=True,
        # allowed_updates=['message', 'edited_message', 'callback_query']  # handle_as_tasks=True, # 🚨
    )


# Запуск асинхронной функции run_bot:
if __name__ == "__main__":
    asyncio.run(run_bot())


