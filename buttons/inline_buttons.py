"""
    Модуль содержит удобные функции формирования инлайновых кнопок.
"""

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Функция для генерации инлайн-кнопок;
def get_callback_btns(*, btns: dict[str, str], sizes: tuple[int, ...] = (2,)):
    """
    sizes: кортеж с числами, определяющими размеры строк.
    По умолчанию это (2,), что означает две кнопки в одной строке.
    *,  # - запрет на передачу не именованных аргументов

    Метод adjust принимает кортеж sizes и настраивает кнопки по строкам в соответствии с указанными размерами.
    Если количество кнопок превышает сумму всех значений в sizes, то:

    Если параметр repeat=True, то размеры из кортежа будут циклически повторяться до тех пор,
    пока не будут размещены все кнопки.
    Если repeat=False (или этот параметр не указан), то оставшиеся кнопки будут сгруппированы в строку по размеру
    последнего элемента в sizes.
    """

    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        # dict_items([('one', 1), ('two', 2), ('three', 3), ('four', 4)]) - пример вида
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


def get_callback_btns_from_tuple(*, btns: list[tuple[str, str]], sizes: tuple[int] = (1,)):
    """
    Передаем список кортежей в функцию = btns !
    *,  # - запрет на передачу не именнованных аргументов
    По умолчанию это (1,), что означает одна кнопка в одной строке.

    Если repeat равно True, используется функция repeat_all для циклического повторения размеров:
    [Button 1]
    [Button 2] [Button 3]
    [Button 4]
    Для adjust(1, 2, repeat=True)

    В противном случае используется repeat_last для использования последнего размера для оставшихся кнопок.
    """
    keyboard = InlineKeyboardBuilder()

    # цикл for будет итерировать по списку кортежей напрямую:
    for key in btns:
        # В списке кортежей элементов больше 2х, по этому обращаемся по индексу
        # Набор данных возвращаемый из запроса: \
        # select(MultiLevelMenu.button_rank, MultiLevelMenu.button_text, MultiLevelMenu.callback_key, ... другие...
        text = key[1]  # = button_text
        data = key[2]  # = callback_key
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    # repeat (bool, по умолчанию False): Флаг, указывающий, следует ли повторять указанные размеры строк,\
    # если кнопок больше, чем суммарное количество размеров в sizes.

    # adjust(оличество кнопок в ряду) , repeat=True
    return keyboard.adjust(*sizes).as_markup()


def get_callback_btns_db_end_optional_btns(*, btns: list[tuple[str, str]], optional_btns: list[tuple[str, str]] = None,
                                           sizes: tuple[int, ...] = (1,)):
    """
    Передаем список кортежей в функцию = btns  и список кортежей доп кнопок ('menu_back_3', 'НАЗАД', 1)

    *,  # - запрет на передачу не именованных аргументов

    По умолчанию это (1,), что означает одна кнопка в одной строке (однако, нужно помнить о наличии доп. кнопок.

    ! optional_btns - механизм включения доп кнопок в выборку кнопок из базы (btns) = их сумма в сообщении.
    optional_btns должен быть типа [('НАЗАД', 'menu_back_3')], что бы легко просуммировать с btns (список кортежей),
    а так же порядок передачи параметров ( 🚨 button_text=key[1], потом callback_key_data=key[2])

    Если repeat равно True, используется функция repeat_all для циклического повторения размеров:
    [Button 1]
    [Button 2] [Button 3]
    [Button 4]
    Для adjust(1, 2, repeat=True)

    В противном случае используется repeat_last для использования последнего размера для оставшихся кнопок.
    """

    keyboard = InlineKeyboardBuilder()

    if optional_btns is None:

        result_btns = btns


    else:

        # Объединяем оба списка
        result_btns = btns + optional_btns  # sum_btns

    # цикл for будет итерировать по списку кортежей напрямую:
    for key in result_btns:
        # В списке кортежей элементов больше 2х, по этому обращаемся по индексу
        # Набор данных возвращаемый из запроса: \
        # select(MultiLevelMenu.button_rank, MultiLevelMenu.button_text, MultiLevelMenu.callback_key, ... другие...
        button_text = key[0]  #
        callback_key_data = key[1]  #
        keyboard.add(InlineKeyboardButton(text=button_text, callback_data=callback_key_data))

    # repeat (bool, по умолчанию False): Флаг, указывающий, следует ли повторять указанные размеры строк,\
    # если кнопок больше, чем суммарное количество размеров в sizes.

    # adjust(количество кнопок в ряду) , repeat=True
    return keyboard.adjust(*sizes).as_markup()


def construct_body_callback(callback_prefix: str | int, payload: str| int):
    """
        Конструктор келбеков создает строку келбека из префикса и необходимой информацией,
        которую можно в последствии использовать для идентификации.
        'callback_constructor'.
    """

    return f'{callback_prefix}{payload}'


def construct_inline_button(inline_keyboard_instance, callback_button_pack: tuple, payload: int | None = None):
    """
        Конструктор inline buttons
    """

    # Распаковка кортежа:
    _text, _callback = callback_button_pack

    # Конструктор callback_data из префикса и полезной нагрузки:
    callback = construct_body_callback(_callback, payload if payload else '')

    inline_keyboard_instance.add(
        InlineKeyboardButton(
            text=_text,
            callback_data=callback
        )
    )


def create_catalog_buttons(task_catalog: list[dict], task_name: str, callback_prefix: str):
    """
        pass
    """

    inline_keyboard_instance: InlineKeyboardBuilder = InlineKeyboardBuilder()

    for itm in task_catalog:

        try:
            # -----------------------------------------
            task_id: int = itm['id']
            # -----------------------------------------
        except Exception as error:
            raise ValueError(
                f'⛔️ Ошибка доступа к значениям по индексу при обработке данных по категориям: {error}')

        construct_inline_button(
            inline_keyboard_instance,
            callback_button_pack=(f'{task_name}_{task_id}', callback_prefix),
            payload=task_id
        )

    return inline_keyboard_instance.adjust(1).as_markup()
