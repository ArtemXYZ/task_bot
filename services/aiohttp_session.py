"""
    Модуль асинхронных методов для http-запросов на основе библиотеки aiohttp.
"""

import time
import aiohttp
import asyncio
# import json

# from custom_support_tools.validators import Validator


# ======================================================================================================================
class AiohttpAdapter:
    """
        Класс содержит кастомные методы для асинхронных http-запросов на основе библиотеки aiohttp.
        RESTAsyncRequestClient

        HTTP-статус коды — это стандартные коды ответов сервера, которые указывают на результат выполнения HTTP-запроса.
        Они делятся на пять классов, каждый из которых обозначает определенный тип ответа.
        Вот полный список статус-кодов:

            1xx: Информационные (Informational)
                Эти коды указывают, что запрос получен и обработка продолжается.

            100 Continue
                Сервер получил начальную часть запроса и ожидает остальные данные.

            101 Switching Protocols
                Сервер соглашается сменить протокол, например, перейти с HTTP на WebSocket.

            102 Processing (WebDAV)
                Запрос принят, но обработка еще не завершена.

            103 Early Hints
                Сервер отправляет часть заголовков, чтобы клиент мог начать предварительную загрузку.

            2xx: Успешные (Success)
                Эти коды указывают, что запрос был успешно обработан.

            200 OK
                Запрос выполнен успешно.

            201 Created
                Запрос выполнен, и новый ресурс создан (например, после POST-запроса).

            202 Accepted
                Запрос принят, но обработка еще не завершена.

            203 Non-Authoritative Information
                Ответ успешен, но информация может быть изменена прокси-сервером.

            204 No Content
                Запрос выполнен, но ответ не содержит тела (например, после DELETE).

            205 Reset Content
                Запрос выполнен, и клиент должен сбросить представление документа.

            206 Partial Content
                Сервер возвращает только часть данных (используется для загрузки файлов по частям).

            207 Multi-Status (WebDAV)
                Ответ содержит несколько статусов для разных частей запроса.

            208 Already Reported (WebDAV)
                Ресурс уже был перечислен в предыдущем ответе.

            226 IM Used
                Сервер выполнил запрос, и ответ содержит результат обработки IM (Instance Manipulation).

            3xx: Перенаправления (Redirection)
                Эти коды указывают, что для завершения запроса требуется дополнительное действие.

            300 Multiple Choices
                Запрос имеет несколько возможных ответов, и клиент должен выбрать один.

            301 Moved Permanently
                Запрошенный ресурс был permanently перемещен на новый URI.

            302 Found
                Запрошенный ресурс временно перемещен на другой URI.

            303 See Other
                Ответ на запрос можно найти по другому URI с помощью GET-запроса.

            304 Not Modified
                Ресурс не был изменен с момента последнего запроса (используется для кэширования).

            305 Use Proxy
                Запрос должен быть выполнен через прокси-сервер.

            306 Switch Proxy (устарел)
                Больше не используется.

            307 Temporary Redirect
                Запрошенный ресурс временно перемещен на другой URI.

            308 Permanent Redirect
                Запрошенный ресурс permanently перемещен на новый URI.

            4xx: Ошибки клиента (Client Errors)
                Эти коды указывают, что запрос содержит ошибку на стороне клиента.

            400 Bad Request
                Запрос содержит синтаксическую ошибку или не может быть обработан.

            401 Unauthorized
                Для доступа к ресурсу требуется аутентификация.

            402 Payment Required
                Зарезервирован для будущего использования.

            403 Forbidden
                Сервер понял запрос, но отказывается его выполнить из-за ограничений доступа.

            404 Not Found
                Запрошенный ресурс не найден на сервере.

            405 Method Not Allowed
                Метод, указанный в запросе, не поддерживается для данного ресурса.

            406 Not Acceptable
                Сервер не может вернуть ответ, соответствующий заголовкам Accept клиента.

            407 Proxy Authentication Required
                Требуется аутентификация на прокси-сервере.

            408 Request Timeout
                Сервер не получил запрос в течение ожидаемого времени.

            409 Conflict
                Запрос конфликтует с текущим состоянием сервера.

            410 Gone
                Запрошенный ресурс больше недоступен, и новый URI не предоставлен.

            411 Length Required
                Сервер требует указать заголовок Content-Length.

            412 Precondition Failed
                Условие, указанное в заголовке запроса, не выполнено.

            413 Payload Too Large
                Тело запроса превышает допустимый размер.

            414 URI Too Long
                URI запроса превышает допустимую длину.

            415 Unsupported Media Type
                Сервер не поддерживает формат данных, указанный в запросе.

            416 Range Not Satisfiable
                Диапазон, указанный в заголовке Range, не может быть выполнен.

            417 Expectation Failed
                Сервер не может выполнить ожидание, указанное в заголовке Expect.

            418 I'm a teapot (шутка)
                Сервер отказывается заваривать кофе в чайнике.

            421 Misdirected Request
                Запрос был направлен на сервер, который не может его обработать.

            422 Unprocessable Entity (WebDAV)
                Запрос содержит семантические ошибки.

            423 Locked (WebDAV)
                Ресурс, к которому обращаются, заблокирован.

            424 Failed Dependency (WebDAV)
                Запрос не выполнен из-за неудачи предыдущего запроса.

            425 Too Early
                Сервер не готов обработать запрос, так как он может быть повторен.

            426 Upgrade Required
                Сервер требует обновления протокола.

            428 Precondition Required
                Сервер требует выполнения условия перед обработкой запроса.

            429 Too Many Requests
                Клиент отправил слишком много запросов за короткое время.

            431 Request Header Fields Too Large
                Заголовки запроса слишком большие для обработки.

            451 Unavailable For Legal Reasons
                Доступ к ресурсу ограничен по юридическим причинам.

            5xx: Ошибки сервера (Server Errors)
                Эти коды указывают, что сервер не смог выполнить запрос из-за внутренней ошибки.

            500 Internal Server Error
                Сервер столкнулся с непредвиденной ошибкой.

            501 Not Implemented
                Сервер не поддерживает функциональность, необходимую для выполнения запроса.

            502 Bad Gateway
                Сервер, выступающий в роли шлюза или прокси, получил недопустимый ответ.

            503 Service Unavailable
                Сервер временно не может обрабатывать запросы (например, из-за перегрузки).

            504 Gateway Timeout
                Сервер, выступающий в роли шлюза или прокси, не дождался ответа от upstream-сервера.

            505 HTTP Version Not Supported
                Сервер не поддерживает версию HTTP, указанную в запросе.

            506 Variant Also Negotiates
                Сервер обнаружил внутреннюю ошибку конфигурации.

            507 Insufficient Storage (WebDAV)
                На сервере недостаточно места для выполнения запроса.

            508 Loop Detected (WebDAV)
                Сервер обнаружил бесконечный цикл при обработке запроса.

            510 Not Extended
                Серверу требуется дополнительная информация для выполнения запроса.

            511 Network Authentication Required
                Клиент должен пройти аутентификацию для доступа к сети
    """

    def __init__(self):
        pass

    @staticmethod
    async def delete_async_response(
            url: str,
            params: dict = None,
            cookies: dict = None,
            headers: dict = None,
            proxy: str = None,
            timeout: int = None,
            mode: str = 'json'
    ) -> object | dict | bytes | str | None:
        """
        Функция для выполнения асинхронных DELETE-запросов с использованием aiohttp.

        :param url: Базовый URL для запроса
        :param params: Параметры запроса (query parameters)
        :param cookies: Словарь cookies для запроса
        :param headers: Словарь заголовков для запроса
        :param proxy: Прокси-сервер для запроса
        :param timeout: Таймаут для запроса в секундах
        :param mode: Режим возвращаемых данных ('json', 'text', 'bytes')
        :return: Ответ в формате JSON, текста, байтов или None в случае ошибки
        """
        try:

            async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
                async with session.delete(
                        url,
                        params=params,
                        proxy=proxy,
                        timeout=aiohttp.ClientTimeout(total=timeout) if timeout else None
                ) as response:
                    if response.status == 200:
                        if mode == 'json':
                            return await response.json()
                        elif mode == 'text':
                            return await response.text()
                        elif mode == 'bytes':
                            return await response.read()
                        else:
                            raise ValueError(
                                f'Ошибка параметра "mode": полученное значение {mode} не валидно. '
                                f'Допустимый синтаксис: "json" (по умолчанию), "text", "bytes".'
                            )
                    else:
                        raise aiohttp.ClientError(f"⛔️ Ошибка HTTP: {response.status} - {await response.text()}")

        except Exception as error_connect:
            raise Exception(f"🆘 Ошибка при выполнении POST-запроса: {error_connect}")


    @staticmethod
    async def post_async_response(
            url: str = None,
            data: dict | str | bytes = None,
            json: dict = None,
            params: dict = None,
            cookies: dict = None,
            headers: dict = None,
            proxy: str = None,
            timeout: int = None,
            mode: str = 'json'
    ) -> object | dict | bytes | str | None:
        """
        Функция для выполнения асинхронных POST-запросов с использованием aiohttp.

        :param url: URL для запроса.
        :param data: Данные для отправки в формате dict, str или bytes (form-data).
        :param json: JSON-данные для отправки (application/json).
        :param params: Параметры запроса (query parameters).
        :param cookies: Словарь cookies для запроса.
        :param headers: Словарь заголовков для запроса.
        :param proxy: Прокси-сервер для запроса.
        :param timeout: Таймаут для запроса.
        :param mode: Режим возвращаемых данных ('json', 'text', 'bytes').
        :return: Ответ в формате JSON, текста, байтов или None в случае ошибки.
        """

        try:
            async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
                async with session.post(
                        url,
                        data=data,
                        json=json,
                        params=params,
                        proxy=proxy,
                        timeout=timeout
                ) as response:
                    if response.status == 200:
                        if mode == 'json':
                            return await response.json()
                        elif mode == 'text':
                            return await response.text()
                        elif mode == 'bytes':
                            return await response.read()
                        else:
                            raise ValueError(
                                f'Ошибка параметра "mode": полученное значение {mode} не валидно. '
                                f'Допустимый синтаксис: "json" (по умолчанию), "text", "bytes".'
                            )
                    else:
                        raise aiohttp.ClientError(f"⛔️ Ошибка HTTP: {response.status} - {await response.text()}")

        except Exception as error_connect:
            raise Exception(f"🆘 Ошибка при выполнении POST-запроса: {error_connect}")


    @staticmethod
    async def get_async_response(
            # self,
            url: str = None,
            params: dict = None,
            cookies: dict = None,
            headers: dict = None,
            proxy: str = None,
            timeout: int = None,
            mode: str = 'json'
    ) -> object | dict | bytes | str | None:
        """
            Функция для выполнения асинхронных запросов с использованием aiohttp.

            :param url: URL для запроса.
            :param params: Параметры запроса (query parameters).
            :param cookies: Словарь cookies для запроса.
            :param headers: Словарь заголовков для запроса.
            :param proxy: Прокси-сервер для запроса.
            :param timeout: Таймаут для запроса.
            :param mode: Режим возвращаемых данных ('json', 'text', 'bytes').
            :return: Ответ в формате JSON, текста, байтов или None в случае ошибки.

            Примечание: валидатор можно не использовать тк. в aiohttp все реализованно,
            за исключением, если не хотим применять кастомные формулировки ошибок.
        """

        try:
            async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:

                async with session.get(url, params=params, proxy=proxy, timeout=timeout) as response:
                    if response.status == 200:
                        if mode == 'json':
                            return await response.json()
                        elif mode == 'text':
                            return await response.text()
                        elif mode == 'bytes':
                            return await response.read()
                        else:
                            raise ValueError(
                                f'Ошибка параметра "mode": полученное значение {mode} не валидно. '
                                f'Допустимый синтаксис: "json" (по умолчанию), "text", "bytes".'
                            )
                    else:
                        raise aiohttp.ClientError(f"⛔️ Ошибка HTTP: {response.status} - {await response.text()}")

        except Exception as error_connect:
            raise Exception(f"🆘 Ошибка при выполнении запроса: {error_connect}")


    async def get_no_disconnect_request(
            self,
            url: str = None,
            params: dict = None,
            cookies: dict = None,
            headers: dict = None,
            proxy: str = None,
            timeout: int = None,
            retries: int = 5,
            gap_retries : int = 120,
            mode: str = 'json'
    ):

        """
            aiohttp.ClientError: базовое исключение для всех ошибок клиента aiohttp.
            aiohttp.ClientConnectionError: ошибка соединения.
            aiohttp.ClientTimeout: если сервер долго не отвечает.
            aiohttp.ClientResponseError: ошибка HTTP ответа.
            asyncio.TimeoutError: таймаут при ожидании ответа.

            Обработка непредвиденных ошибок: Если возникает ошибка, не связанная с потерей соединения или таймаутом,
            она будет обработана блоком except aiohttp.ClientError, что предотвратит аварийное завершение программы.
        """

        attempt = 0  # Количество попыток

        while attempt < retries:

            if attempt > 0:
                print(f"♻️ Повторное соединение, попытка: {attempt} / из {retries}.")

            try:
                # Основной запрос:
                data = await self.get_async_response(
                    url=url,
                    params=params,
                    cookies=cookies,
                    headers=headers,
                    proxy=proxy,
                    timeout=timeout,
                    mode=mode
                )
                return data  # Возвращаем данные, если успешен

            except (
                    aiohttp.ClientConnectionError,
                    aiohttp.ClientTimeout,
                    asyncio.TimeoutError
            ) as e:
                # Обработка ошибок соединения
                attempt += 1
                print(
                    f"🆘 Ошибка соединения: {e}. Попытка {attempt}/{retries}."
                    f"🕑 Повтор через {gap_retries} сек."
                )
                time.sleep(gap_retries)  # Тайм-аут перед повторной попыткой

            except  aiohttp.ClientResponseError as e:
                # Обработка HTTP ошибок
                print(f"HTTP ошибка: {e}. Попытка {attempt + 1}/{retries}.")
                attempt += 1
                time.sleep(gap_retries)

            except Exception as e:
                # Обработка любых других ошибок
                print(f"Непредвиденная ошибка: {e}. Прерывание.")
                return None

            print("Не удалось выполнить запрос после нескольких попыток.")
            return None

    def __str__(self):
        return (
            f'{self.__class__.__name__}'
        )

    def __repr__(self):
        return (
            f'{self.__class__.__name__}'
        )
