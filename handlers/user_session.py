"""
    Основной модуль диалогов и взаимодействия с пользователями.
"""
import datetime
from typing import List

# -------------------------------- Стандартные модули
import re
# -------------------------------- Сторонние библиотеки
from aiogram import Bot, types
from aiogram.types import Message, CallbackQuery

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter, CommandObject, or_f

# -------------------------------- Локальные модули

from services.aiohttp_session import AiohttpAdapter
from states.states import *
from buttons.inline_buttons import *  # Кнопки встроенного меню - для сообщений
from buttons.keyboard_buttons import *  # Кнопки встроенного меню - для сообщений
from config.replicas import *

# Назначаем роутер для всех типов чартов:
main_router = Router()
aiohttp_adapter = AiohttpAdapter()
HEADERS = {"Content-Type": "application/json"}
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
@main_router.message((F.text == SHOW_TASKS) | (F.text == '/show_tasks'))
async def show_tasks(message: Message, state: FSMContext, bot: Bot):
    """
        Ответ на кнопку '🔍 ПОКАЗАТЬ ЗАДАЧИ'.
    """

    try:

        # Запрос к API на список задач:
        task_catalog: dict = await aiohttp_adapter.get_async_response(
            url='http://localhost:8000/api/tasks/list',
            headers=HEADERS
        )

        task_list = task_catalog.get('task_list')

        if not task_list:
            message_text = "📭 Хранилище пусто, задачи еще не были добавлены."
        else:
            tasks_text = "\n".join(
                f"{i+1}. {task['task']} (до {task['deadline']})"
                for i, task in enumerate(task_list)
            )
            message_text = f"📋 Список задач:\n\n🔻  {tasks_text}"

        await message.reply(
            text=message_text,
            reply_markup=get_keyboard(
                ADD_TASK,
                DELETE_TASK,
                SHOW_TASKS,
                START,
                placeholder="Введите команду",
                sizes=(1, 1, 1, 1)
            )
        )

    except Exception as error:
        print(error)

        await message.reply(
            text=f'💬 Ошибка запроса списка задач, подробности:\n\n'
                 f'🔻 {error}',
            reply_markup=get_keyboard(
                ADD_TASK,
                DELETE_TASK,
                SHOW_TASKS,
                START,
                placeholder="Введите команду",
                sizes=(1, 1, 1, 1)
            )

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
        task_catalog: dict = await aiohttp_adapter.get_async_response(
            url='http://localhost:8000/api/tasks/list',
            headers=HEADERS
        )

        task_list = task_catalog.get('task_list')

        if task_list:

            await message.reply(
                text=f'💬 Выберите, какую необходимо удалить!',
                reply_markup=create_catalog_buttons(
                    task_catalog.get('task_list'),
                    task_name='Задача ',
                    callback_prefix='del_task_'
                )
            )

        else:

            await message.reply(
                text='📭 Хранилище пусто, задачи еще не были добавлены, удалять нечего!',
                reply_markup=get_keyboard(
                    ADD_TASK,
                    DELETE_TASK,
                    SHOW_TASKS,
                    START,
                    placeholder="Введите команду",
                    sizes=(1, 1, 1, 1)
                )
            )

    except Exception as error:
        print(error)

        await message.reply(
            text=f'💬 Ошибка запроса списка задач, подробности:\n\n'
                 f'🔻 {error}',
            reply_markup=get_keyboard(
                ADD_TASK,
                DELETE_TASK,
                SHOW_TASKS,
                START,
                placeholder="Введите команду",
                sizes=(1, 1, 1, 1)
            )
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

    # Получить callback, номер айди:
    # Ищем число в конце строки
    match = re.search(r'\d+$', callback.data)
    task_id = match.group()

    try:

        response = await aiohttp_adapter.delete_async_response(
            url=f'http://localhost:8000/api/tasks/delete/{task_id}',
            headers=HEADERS
        )

        await callback.message.edit_text(
            text=f'💬 Задача успешно удалена!\n\n🔻 Подробности: {response}',
        )

    except Exception as error:
        print(
            f'⛔️ Ошибка: {error}'
        )

        await callback.message.edit_text(
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

    # response: None | dict = None

    deadline_message_text = message.text

    # Получаем данные:
    data_state_dict = await state.get_data()
    task_message_text = data_state_dict.get('task_message_text')

    payload = {
        'task': task_message_text,
        'deadline': deadline_message_text,
    }
    # ------------------------- 1 / Ошибки запроса:
    try:
        # Запрос на сервер и подтверждение добавления (пришлет ответ):
        response = await aiohttp_adapter.post_async_response(
            url='http://localhost:8000/api/tasks/add',
            json=payload,
            headers=HEADERS
        )

        # ------------------------- При успехе:
        id_task = response.get('id')

        await message.reply(
            text=f'💬 Задача успешно добавлена!\n\n'
                 f'🔻 Подробности:\n'
                 f' 🔹 Id: [{id_task}]\n'
                 f' 🔹 Задача:\n'
                 f' [{task_message_text}]\n'
                 f' 🔹 Дедлайн:\n'
                 f' [{deadline_message_text}]\n',
            reply_markup=get_keyboard(
                ADD_TASK,
                DELETE_TASK,
                SHOW_TASKS,
                START,
                placeholder="Введите команду",
                sizes=(1, 1, 1, 1)
            )
        )

    except Exception as error:

        print(error)
        await message.reply(
            text=f'💬 Ошибка запроса на добавление задачи, подробности:\n\n'
                 f'🔻 {error}',
            reply_markup=get_keyboard(
                ADD_TASK,
                DELETE_TASK,
                SHOW_TASKS,
                START,
                placeholder="Введите команду",
                sizes=(1, 1, 1, 1)
            )
        )

    await state.clear()
# ----------------------------------------------- ADD_TASK




#
# # ------------------------- 2 / Ошибки валидации:
# if response:
#
#     # Проверка статуса ошибки:
#     detail = response.get('detail')
#
#     if detail:
#         print(
#             f'⛔️ Ошибка валидации входных данных, подробности:\n\n'
#             f'🔻  {detail}'
#         )
#
#         await message.reply(
#             text=f'⛔️ Ошибка валидации входных данных, подробности:\n\n'
#                  f'🔻  {detail}',
#             reply_markup=get_keyboard(
#                 ADD_TASK,
#                 DELETE_TASK,
#                 SHOW_TASKS,
#                 START,
#                 placeholder="Введите команду",
#                 sizes=(1, 1, 1, 1)
#             )
#         )
#
# else: