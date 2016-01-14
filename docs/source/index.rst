.. toctree::
   :maxdepth: 2


Локализация
==================
Accept-Language: <en|ru|...>


Возможные типы продуктов
==================
VEGAN, VEGETARIAN, LACTOVEGETARION, FISH, MEAT

API
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
            "qrcode": "some-qr-code",
        },
	    "category": {
	        "id": "category",
	        "title": "Some sub category",
	        "sub_category": {
	            "id": "subcategory",
	            "title": "Some sub category"
	        }
	    }
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
	    "producer": "Microsoft",
	    "category": {
	        "id": "category",
	        "title": "Some sub category",
	        "sub_category": {
	            "id": "subcategory",
	            "title": "Some sub category"
	        }
	    }
	}

Пример ответа:
::
	{
	    "id": 1,
	    "title": "Some good",
	    "info": "vegan",
	    "producer": "Microsoft",
	    "category": {
	        "id": "category",
	        "title": "Some sub category",
	        "sub_category": {
	            "id": "subcategory",
	            "title": "Some sub category"
	        }
	    }
	}

add: Добавление изображения к товару
------------------

Запрос:
::
  [POST|MULTIPART] /api/v1.0/add/<productId>/image

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
       "1": "Category 1",
       "3": "Category 3"
   }


categories: Получения детализации категории
------------------

Запрос:
::
   [GET] /api/v1.0/categories/<categoryId>

Пример ответа:
::
   {
       "id": "1"
       "title": "Catgory title",
       "children": {
           "4": "Subcategory title"
           "5": "Subcategory title"
       },
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
