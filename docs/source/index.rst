.. toctree::
   :maxdepth: 2

Evegano server API
==================

Локализация
------------------
Accept-Language: <en|ru|...>


Общий формат запроса
------------------

HTTP статус всегда имеет значение 200, в том числе и при неуспешных/некорректных запросах.

Если статус не равен 200, значит сервер не справился с обработкой запроса.

Каждый ответ сервера всегда содержит поля error_code и error_message.

Если запрос успешен, то error_code будет содержать значение 0, error_message будет содержать null, а поле result собственно содержание ответа.

Пример:
::
    {
        'error_code': 0 ,
        'error_message': null,
        'result': ...
    }

В примерах, которые можно найти ниже опускается уровень ошибок и приводится сразу значение result.

Общие для всех запросов ошибки:

==========  =============
error_code  error_message
==========  =============
0           null
-2          Expected content type: "application/json".
-3          No JSON object could be decoded.
-5          Expected parameter <PARAMETER_NAME>
-5          Expected parameters: <PARAM1>, <PARAM2>, ...
-11         The parameter <PARAMETER_NAME> should be ...
==========  =============

Остальные коды ошибок описаны в конкретных запросах.

Запросы
==================

check: Проверка товара
------------------

Возможные значения поля info: vegan, vegeterian, fish, meat, milk, unknown

Запрос:
::
  [GET] /api/v1.0/check

Параметры:
::
  code=<string>
  type=<barcode|qrcode>

Возможные ошибки:

==========  =============
error_code  error_message
==========  =============
-7          Product code not found.
==========  =============

Пример ответа:
::
    {
        "id": 1,
        "title": "Some good",
        "info": "vegan",
        "photo": "http://example.com/some.png",
        "producer": {
            "title": "Microsoft",
            "ethical": bool
        },
        "codes": [
            {"type": "barcode", "code": "some-bar-code"},
            {"type": "qrcode", "code": "some-qr-code"}
        ],
        "category": {
            "id": 1,
            "title": "Some sub category",
            "parent": {
                "id": 2,
                "title": "Some category"
            }
        }
    }

add-producer: Добавление производителя
------------------

Параметр ethical может быть null, либо его можно не передавать.

Возможные ошибки:

==========  =============
error_code  error_message
==========  =============
-11          The parameter ethical should be bool or null
==========  =============


Запрос:
::
  [POST] /api/v1.0/add-producer


Пример запроса:
::
    {
        "title": "Some good",
        "ethical": true
    }

Пример ответа:
::
    {
        "id": 1,
        "title": "Microsoft",
        "ethical": true
    }

add: Добавление товара
------------------

Запрос:
::
  [POST] /api/v1.0/add

==========  =============
error_code  error_message
==========  =============
-13         Product code already exists
==========  =============

Пример запроса:
::
    {
        "title": "Some good",
        "info": "vegan",
        "code_type": "barcode",
        "code": "barcode-value",
        "producer_id": 1,
        "category_id": 15
    }

Пример ответа:
::
    {
        "id": 1,
        "title": "Some good",
        "info": "vegan",
        "producer": {
            "id": 1,
            "title": "Microsoft"
            "ethical": null,
        },
        "photo": null,
        "codes": [{"type": "barcode", "barcode-value"}],
        "category": {
            "id": 1,
            "title": "Some sub category",
            "parent": {
                "id": 2,
                "title": "Some category"
            }
        }
    }

add: Добавление фотографии к товару
------------------

Запрос:
::
  [POST|MULTIPART] /api/v1.0/add/<productId>/photo

Возможные ошибки:

==========  =============
error_code  error_message
==========  =============
-5          No image was sent.
-7          Product not found.
==========  =============


Пример ответа:
::
    {
        "url": "http://example.com/some.png"
    }

complain: Жалоба на тип товара
------------------

Запрос:
::
   [POST] /api/v1.0/<productId>/complain

Пример запроса:
::
    {
        "message": "VI VSIE VRETE"
    }

Возможные ошибки:

==========  =============
error_code  error_message
==========  =============
-7          Product code not found.
==========  =============


Пример ответа:
::
    null


categories: Получения категорий верхнего уровня
------------------

Запрос:
::
   [GET] /api/v1.0/categories/

Пример ответа:
::
   [
       {"id": 1, "title": "Category 1"},
       {"id": 2, "title": "Category 2"}
   ]



categories: Получения детализации категории
------------------

Запрос:
::
   [GET] /api/v1.0/categories/<categoryId>

Возможные ошибки:

==========  =============
error_code  error_message
==========  =============
-17         Category not found.
==========  =============

Пример ответа:
::
   {
       "id": "1"
       "title": "Catgory title",
       "children": [
           {"id": "4", "title": "Subcategory title"},
           {"id": "5", "title": "Subcategory title"}
       ],
   }

producers: Получение списка производителей
------------------

Запрос:
::
   [GET] /api/v1.0/producers/

Параметры:
::
  title=<string>

Пример ответа:
::
    [
        {
            "id": 1,
            "ethical": false,
            "title": "Microsoft"
        },
        {
            "id": 1,
            "ethical": false,
            "title": "Meta Company"
        }
    ]

..
   Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`
