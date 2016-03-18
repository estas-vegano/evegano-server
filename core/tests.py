import json
from django.test import TestCase
from django.test import Client
from django.conf import settings
import models

class ApiBase(TestCase):

    def setUp(self):
        self.client = Client()
        self.maxDiff = None

    def _post_json(self, url, data):
        return self.client.post(url,
                               json.dumps(data),
                               content_type="application/json")

    def create_producer(self, title):
        producer = models.Producer()
        producer.save()
        producer_title = models.ProducerTitle(
            producer=producer,
            lang=settings.DEFAULT_LANGUAGE,
            title=title
        )
        producer_title.save()

        return producer

    def create_category(self, title, parent=None):
        category = models.Category(parent=parent)
        category.save()
        category_title = models.CategoryTitle(
            category=category,
            lang=settings.DEFAULT_LANGUAGE,
            title=title
        )
        category_title.save()
        return category

    def create_product(self, codes=[]):
        category = self.create_category('Some category')

        producer = self.create_producer('Some producer')
        product = models.Product(
            info='vegan',
            producer=producer,
            category=category
        )
        product.save()

        for type, code in codes:
            product_code = models.ProductCode(product=product,
                                              type=type,
                                              code=code)
            product_code.save()
        return product

class ApiTestCase(ApiBase):

    def test_add_wrong_content_type(self):
        paths = [
            '/api/v1/add',
            '/api/v1/add-producer',
        ]
        for path in paths:
            response = self.client.post('/api/v1/add',
                                        json.dumps({}),
                                        content_type="wrong")
            self.assertEquals(
                json.loads(response.content),
                {'error': 'Expected content type: "application/json".'}
            )

    def test_wrong_json(self):
        paths = [
            '/api/v1/add',
            '/api/v1/add-producer',
        ]
        for path in paths:
            response = self.client.post(path,
                                        'wrong-json',
                                        content_type="application/json")
            self.assertEquals(
                json.loads(response.content),
                {'error': 'No JSON object could be decoded.'}
            )

    def test_check(self):
        expected_err = {"error": "Expected args: code, type."}
        not_found_err = {"error": "Not found."}

        product = self.create_product(codes=[('barcode', 'code'), ])
        product_data = {
            u'id': product.id,
            u'info': u'vegan',
            u'category': {
                u'id': product.category.id,
                u'title': u'Some category'
            },
            u'codes': {
                u'barcode': u'code'
            },
            u'producer': {
                u'id': product.producer.id,
                u'ethical': None,
                u'title': u'Some producer'
            },
            u'title': None,
            u'photo': None,
        }
        cases = [
            ({}, expected_err, 400),
            ({'code': '123'}, expected_err, 400),
            ({'type': 'barcode'}, expected_err, 400),
            ({'code': 'unknown', 'type': 'barcode'}, not_found_err, 404),
            ({'code': 'code', 'type': 'barcode'}, product_data, 200),
        ]

        for args, expected_err, expected_code in cases:
            response = self.client.get('/api/v1/check', args)
            self.assertEquals(
                json.loads(response.content),
                expected_err
            )
            self.assertEquals(response.status_code, expected_code)

    def test_add_producer(self):
        cases = [({"title": "Some good 1",
                   "ethical": True},
                  {"ethical": True,
                   "id": 1,
                   "title": "Some good 1"}),

                 ({"title": "Some good 2",
                   "ethical": False},
                  {"ethical": False,
                   "id": 2,
                   "title": "Some good 2"}),

                 ({"title": "Some good 3",
                   "ethical": None},
                  {"ethical": None,
                   "id": 3,
                   "title": "Some good 3"}),

                 ({"title": "Some good 4"},
                  {"ethical": None,
                   "id": 4,
                   "title": "Some good 4"}),]

        for data, expected in cases:
            response = self._post_json('/api/v1/add-producer', data)

            self.assertEquals(json.loads(response.content), expected)

    def test_add(self):
        category = models.Category()
        category.save()
        producer = models.Producer.create(
            settings.DEFAULT_LANGUAGE,
            {'title': 'some-product', 'ethical': True}
        )

        data = {
            "title": "Some good",
            "info": "vegan",
            "producer_id": producer.id,
            "category_id": category.id
        }
        response = self._post_json('/api/v1/add', data)

        self.assertEqual(
            json.loads(response.content),
            {u'id': models.Product.objects.last().id,
             u'info': u'vegan',
             u'category': {u'id': category.id, u'title': u''},
             u'codes': {},
             u'producer': {u'id': producer.id,
                           u'ethical': True,
                           u'title': u'some-product'},
             u'title': u'Some good',
             u'photo': None,}
        )

    def test_categories(self):
        self.create_category('Category 1')
        self.create_category('Category 2')
        self.create_category('Category 3')
        response = self.client.get('/api/v1/categories/')
        categories = json.loads(response.content)['categories']
        categories.sort()
        self.assertEquals(
            categories,
            [{u'id': 1, u'title': u'Category 1'},
             {u'id': 2, u'title': u'Category 2'},
             {u'id': 3, u'title': u'Category 3'}]
        )

    def test_category(self):
        c1 = self.create_category('Category 1')
        c2 = self.create_category('Subcategory 2', parent=c1)
        c3 = self.create_category('Subcategory 3', parent=c1)
        c4 = self.create_category('Subcategory 4', parent=c1)

        response = self.client.get('/api/v1/categories/' + str(c1.id))
        self.assertEquals(
            json.loads(response.content),
            {
                "id": c1.id,
                "title": "Category 1",
                "children": [
                    {'id': c2.id, 'title': "Subcategory 2"},
                    {'id': c3.id, 'title': "Subcategory 3"},
                    {'id': c4.id, 'title': "Subcategory 4"}
                ],
            }
        )

    def test_producers(self):
        p1 = self.create_producer('Producer 1')
        p2 = self.create_producer('Producer 2')
        p3 = self.create_producer('Producer 3')
        p4 = self.create_producer('Some really other producer')
        response = self.client.get('/api/v1/producers/')

        self.assertEquals(
            json.loads(response.content),
            {"producers": [
                {"id": p1.id,
                 "ethical": None,
                 "title": "Producer 1"},
                {"id": p2.id,
                 "ethical": None,
                 "title": "Producer 2"},
                {"id": p3.id,
                 "ethical": None,
                 "title": "Producer 3"},
                {"id": p4.id,
                 "ethical": None,
                 "title": "Some really other producer"}]},
        )

        response = self.client.get('/api/v1/producers/', {'title': 'Pro'})
        self.assertEquals(
            json.loads(response.content),
            {"producers": [
                {"id": p1.id,
                 "ethical": None,
                 "title": "Producer 1"},
                {"id": p2.id,
                 "ethical": None,
                 "title": "Producer 2"},
                {"id": p3.id,
                 "ethical": None,
                 "title": "Producer 3"},]}
        )
