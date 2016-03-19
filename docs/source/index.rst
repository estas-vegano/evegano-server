.. toctree::
   :maxdepth: 2

Evegano server API
==================

Локализация
------------------
Accept-Language: <en|ru|...>


Возможные типы продуктов
------------------
VEGAN, VEGETARIAN, LACTOVEGETARION, FISH, MEAT

Ошибки
------------------
Обработку ошибок следует начинать с анализа HTTP статуса.
Могут быть следующие варианты:

* Запрос завершился успешно, HTTP статус равен 200.

* Запрос завершился нефатальной ошибкой, HTTP статус отличен от 200 и тело ответа содержит валидный json.

* Запрос заверишлся фатальной ошибкой приложения или до выполненния приложения не дошло, HTTP статус равен 5XX, тело ответа не содержит валидного json.


Ответ нефатальных ошибок имеет вид:
::
   {'error': 'error description'}

Данное сообщение об ошибке не локализовано и не предназначено для показа пользователю. Его назначение - удобство в отладке, поведение приложения же рекомендуется основывать на HTTP статусах.

Общие для всех запросов нефатальные ошибки:

* HTTP статус 400, значение error: 'Expected content type: "application/json".'

* HTTP статус 400, значение error: 'No JSON object could be decoded.'

Статусы остальных возможных нефатальных ошибок описаны в конкретных запросах.


Запросы
==================

check: Проверка товара
------------------

Запрос:
::
  [GET] /api/v1.0/check

Параметры:
::
  code=<string>
  type=<barcode|qrcode>

Возможные ошибки:

* HTTP статус 400, значение error: 'Expected args: code, type.'

* HTTP статус 404, код отсуствует в базе. Значение error: 'Not found'

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
        "codes": {
            "barcode": "some-bar-code",
            "qrcode": "some-qr-code"
        },
        "category": {
            "id": 1,
            "title": "Some sub category",
            "sub_category": {
                "id": 2,
                "title": "Some sub category"
            }
        }
    }

add: Добавление производителя
------------------

Параметр ethical может быть null, либо его можно не передавать.

Возможные ошибки:

* HTTP статус 400, значение error: 'Parameter ethical must be bool or null'

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

Пример запроса:
::
    {
        "title": "Some good",
        "info": "vegan",
        "producer_id": 1,
        "category_id": 15
    }

Пример ответа:
::
    {
        "id": 1,
        "title": "Some good",
        "info": "vegan",
        "producer": "Microsoft",
        "category": {
            "id": 1,
            "title": "Some sub category",
            "sub_category": {
                "id": 2,
                "title": "Some sub category"
            }
        }
    }

add: Добавление фотографии к товару
------------------

Запрос:
::
  [POST|MULTIPART] /api/v1.0/add/<productId>/photo

Возможные ошибки:

* HTTP статус 404, товар отсуствует в базе. Значение error: 'Not found'

* HTTP статус 400, изображение не передано. Значение error: 'No image was sent.'


Пример ответа:
::
    {
        "photo":"http://example.com/some.png"
    }

complain: Жалоба на тип товара
------------------

Запрос:
::
   [POST] /api/v1.0/<productId>/complain

Пример запроса:
::
    {
        "message":"VI VSIE VRETE"
    }


categories: Получения категорий верхнего уровня
------------------

Запрос:
::
   [GET] /api/v1.0/categories/

Пример ответа:
::
   {
       "categories": [
           {"id": 1, "title": "Category 1"},
           {"id": 2, "title": "Category 2"}
       ]
   }


categories: Получения детализации категории
------------------

Запрос:
::
   [GET] /api/v1.0/categories/<categoryId>

Возможные ошибки:

* HTTP статус 404, категория отсуствует в базе. Значение error: 'Not found'

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
   {
       "producers": [
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
   }

..
   Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`
