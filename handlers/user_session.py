"""
    Основной модуль диалогов и взаимодействия с пользователями.
"""
import datetime
from typing import List

# -------------------------------- Стандартные модули
# from string import punctuation
# import traceback
# -------------------------------- Сторонние библиотеки
from aiogram import Bot, types
from aiogram.types import Message, CallbackQuery

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter, CommandObject, or_f

# -------------------------------- Локальные модули
from filters.chats_filters import ChatTypeFilter
from states.states import *
from buttons.inline_buttons import *  # Кнопки встроенного меню - для сообщений
from buttons.keyboard_buttons import *  # Кнопки встроенного меню - для сообщений
from config.replicas import *

# Назначаем роутер для всех типов чартов:
main_router = Router()


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------- Главное меню
# Прием СТАРТА / Примет только кнопку старт
# @main_router.message(or_f(CommandStart(), F.text == START))
@main_router.message(CommandStart())  # Обработка /start
@main_router.message(F.text == START)  # Обработка текста "SHOW_TASKS"
async def start(message: Message, state: FSMContext, bot: Bot):
    """
        Старт бота, вывод приветствия и инструкций.
    """

    tg_id = message.from_user.id

    # Отправляем приветствие.
    await message.reply(
        text=f'💬 {WELCOME_TEXT}',
        reply_markup=get_keyboard(
            ADD_TASK,
            DELETE_TASK,
            SHOW_TASKS,
            START,
            placeholder="Введите команду",
            sizes=(1, 1, 1, 1)
        )
    )

    # -------------------- Вывод в консоль служебной информации:
    print(f'Старт бота tg_id пользователя: [{tg_id}]')


# ----------------------------------------------- SHOW_TASKS
@main_router.message(F.text == SHOW_TASKS)
async def show_tasks(message: Message, state: FSMContext, bot: Bot):
    """
        Ответ на кнопку '🔍 ПОКАЗАТЬ ЗАДАЧИ'.
    """

    # #  todo 3.1 вводит список задач :
    # 1. Сделать отчет (дедлайн: 25.11.2024)
    # 2. Купить продукты (дедлайн: 20.11.2024)

    # запрос к API
    pass
    #  todo 3. Пользователь вводит /show_tasks бот получает список задач от API:
    # Запрос к API на список задач:
    # tasks: dict = {}

    # task_list: list= [key, value  for tasks]

    task_list = []

    # Проверка статуса ошибки:
    if task_list:

        await message.reply(
            text=f'💬 Список задач:\n\n'
                 f'🔻 {task_list if task_list else 'Хранилище пусто, задачи еще не были добавлены.'}',
        )

    else:

        await message.reply(
            text=f'💬 Ошибка запроса списка задач, подробности:\n\n'
                 f'🔻 {task_list }',
        )

# ----------------------------------------------- SHOW_TASKS

# ----------------------------------------------- DELETE_TASK
@main_router.message(F.text == DELETE_TASK)
async def start_delete_task(message: Message, state: FSMContext, bot: Bot):
    """
        Ответ на кнопку '➖ УДАЛИТЬ ЗАДАЧУ'.
    """

    try:
        #  Запрос к API на список задач:
        task_catalog = []

        await message.reply(
            text=f'💬 Выберите, какую необходимо удалить!',
            reply_markup=create_catalog_buttons(
                task_catalog,
                task_name='Задача ',
                callback_prefix='del_task_'
            )
        )


    except Exception as error:
        print(
            f'⛔️ Ошибка: {error}'
        )

        await message.reply(
            text=f'💬 Ошибка запроса списка задач, подробности:\n\n'
                 f'🔻 {error}',
        )


    # Устанавливаем состояние:
    await state.set_state(Task.delete_task)


@main_router.callback_query(StateFilter(Task.delete_task), F.data.startswith('del_task_'))
async def delete_task(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
        Принимает запрос на удаление от пользователя
    """

    # Ответ на сервер, что кнопку нажали.
    await callback.answer()

    try:
        #  Запрос к API на список задач:
        task_catalog = []

        await callback.reply(
            text=f'💬 Задача успешно удалена!'
        )

    except Exception as error:
        print(
            f'⛔️ Ошибка: {error}'
        )

        await callback.reply(
            text=f'💬 Ошибка удаления задачи, подробности:\n\n'
                 f'🔻 {error}',
        )
# ----------------------------------------------- DELETE_TASK

# ----------------------------------------------- ADD_TASK
@main_router.message(F.text == ADD_TASK)
async def add_task(message: Message, state: FSMContext, bot: Bot):
    """
        Ответ на кнопку '➕ ДОБАВИТЬ ЗАДАЧУ'.
    """

    await message.reply(
        text=f'💬 Введите название задачи!',
        # Удаляем клавиатуру:
        reply_markup=types.ReplyKeyboardRemove()  # Удаляет клавиатуру
        #
    )

    # Устанавливаем состояние:
    await state.set_state(Task.task_data)


@main_router.message(StateFilter(Task.task_data))
async def set_task(message: Message, state: FSMContext, bot: Bot):
    """
        Принимает новую ЗАДАЧУ. Ожидаем состояние: Task.task_data.
    """

    task_message_text = message.text


    await message.reply(
        text=f'💬 Введите дедлайн (ДД.ММ.ГГГГ)!',
    )

    # Устанавливаем состояние:
    await state.set_state(Task.deadline)
    await state.update_data(task_message_text=task_message_text)


@main_router.message(StateFilter(Task.deadline))
async def set_deadline(message: Message, state: FSMContext, bot: Bot):
    """
        Принимает новую ЗАДАЧУ. Ожидаем состояние: Task.task_data.
    """

    deadline_message_text = message.text

    # Получаем данные:
    data_state_dict = await state.get_data()
    task_message_text = data_state_dict.get('task_message_text')

    payload = {
        'task': task_message_text,
        'deadline': deadline_message_text,
    }

    print(
        f'Имитация отправки в хранилище данных \n'
        f' {payload}'
    )

    # Запрос пост через апи.
    # todo Бот отправляет запрос на сервер и подтверждает добавление.
    pass


    task_list = True

    # Проверка статуса ошибки:
    if task_list:

        await message.reply(
            text=f'💬 Задача успешно добавлена!\n\n'
                 f'🔻 Подробности:\n'
                 f' 🔹 Задача:\n'
                 f' {task_message_text}\n'
                 f' 🔹 Дедлайн:\n'
                 f' {deadline_message_text}\n',
            reply_markup=get_keyboard(
                ADD_TASK,
                DELETE_TASK,
                SHOW_TASKS,
                START,
                placeholder="Введите команду",
                sizes=(1, 1, 1, 1)
            )
        )

    else:

        await message.reply(
            text=f'💬 Ошибка запроса на добавление задачи, подробности:\n\n'
                 f'🔻 {task_list}',
        )

    await state.clear()

# ----------------------------------------------- ADD_TASK




