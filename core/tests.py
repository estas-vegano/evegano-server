import json
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory
from django.test import Client
from django.conf import settings
import models
import core.views as views

class ApiBase(TestCase):

    def setUp(self):
        self.client = Client()
        self.maxDiff = None
        self.factory = RequestFactory()

    def _post_json(self, url, data):
        return self.client.post(
            url,
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
        c1 = self.create_category('Category 1')
        c2 = self.create_category('Subcategory 2', parent=c1)

        producer = self.create_producer('Some producer')
        product = models.Product(
            info='vegan',
            producer=producer,
            category=c2
        )
        product.save()

        for type, code in codes:
            product_code = models.ProductCode(
                product=product,
                type=models.CodeType.objects.get_or_create(name=type)[0],
                code=code
            )
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
                {'error_code': -2,
                 'error_message': 'Expected content type: "application/json".'}
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
                {'error_code': -3,
                 'error_message': 'No JSON object could be decoded.'}
            )

    def test_check(self):
        expected_err = {"error_code": -5,
                        "error_message": "Expected parameters: code, type."}
        not_found_err = {"error_code": -7,
                         "error_message": "Product code not found."}

        product = self.create_product(codes=[('barcode', 'code'), ])
        product_data = {
            'error_code': 0,
            'error_message': None,
            'result': {
                u'id': product.id,
                u'info': u'vegan',
                u'category': {
                    u'id': product.category.id,
                    u'title': u'Subcategory 2',
                    u'parent': {
                        u'id': product.category.parent.id,
                        u'title': u'Category 1',
                    }
            },
            u'codes': [
                {'type': u'barcode', 'code': u'code'}
            ],
            u'producer': {
                u'id': product.producer.id,
                u'ethical': None,
                u'title': u'Some producer'
            },
            u'title': None,
                u'photo': None,
            }
        }
        cases = [
            ({}, expected_err, 200),
            ({'code': '123'}, expected_err, 200),
            ({'type': 'barcode'}, expected_err, 200),
            ({'code': 'unknown', 'type': 'barcode'}, not_found_err, 200),
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
                   "title": "Some good 4"}),

                 ({"title": "Some good 5",
                   "ethical": 1},
                  {"ethical": True,
                   "id": 5,
                   "title": "Some good 5"}),]

        for data, expected in cases:
            response = self._post_json('/api/v1/add-producer', data)

            self.assertEquals(json.loads(response.content)['result'],
                              expected)

    def test_add_producer_wrong_ethical(self):
        data = {"title": "Some good 3",
                "ethical": 'WAATT'}
        response = self._post_json('/api/v1/add-producer', data)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            json.loads(response.content),
            {"error_code": -11,
             "error_message": "The parameter ethical should be bool or null"}
        )

    def test_add(self):
        category_parent = self.create_category('Category')
        category = self.create_category('Subcategory',
                                        parent=category_parent)

        producer = models.Producer.create(
            settings.DEFAULT_LANGUAGE,
            {'title': 'some-producer', 'ethical': True}
        )

        data = {
            "title": "Some good",
            "info": "vegan",
            "code_type": "barcode",
            "code": "barcode-value",
            "producer_id": producer.id,
            "category_id": category.id
        }
        response = self._post_json('/api/v1/add', data)

        self.assertEqual(
            json.loads(response.content)['result'],
            {u'id': models.Product.objects.last().id,
             u'info': u'vegan',
             u'category': {
                 u'id': category.id,
                 u'title': 'Subcategory',
                 u'parent': {
                     u'id': category.parent.id,
                     u'title': 'Category',
                 }
             },
             u'codes': [{'type': 'barcode', 'code': 'barcode-value'}],
             u'producer': {u'id': producer.id,
                           u'ethical': True,
                           u'title': u'some-producer'},
             u'title': u'Some good',
             u'photo': None,}
        )

    def test_add(self):
        factory = RequestFactory()
        category_parent = self.create_category('Category')
        category = self.create_category('Subcategory',
                                        parent=category_parent)

        producer = models.Producer.create(
            settings.DEFAULT_LANGUAGE,
            {'title': 'some-producer', 'ethical': True}
        )

        data = {
            "title": "Some good",
            "info": "vegan",
            "code_type": "barcode",
            "code": "barcode-value",
            "producer_id": producer.id,
            "category_id": category.id
        }
        request = factory.post(
            '/api/v1/add', json.dumps(data),
            content_type="application/json")
        request.LANGUAGE_CODE = 'some-custom-lang'
        response = views.add(request)

        pc = models.ProductCode.objects.get(code="barcode-value")
        self.assertEquals(pc.product.get_title('some-custom-lang'),
                          "Some good")

    def test_add_wo_title(self):
        category_parent = self.create_category('Category')
        category = self.create_category('Subcategory',
                                        parent=category_parent)

        producer = models.Producer.create(
            settings.DEFAULT_LANGUAGE,
            {'title': 'some-producer', 'ethical': True}
        )

        data = {
            "info": "vegan",
            "code_type": "barcode",
            "code": "barcode-value",
            "producer_id": producer.id,
            "category_id": category.id
        }
        response = self._post_json('/api/v1/add', data)
        self.assertEquals(
            json.loads(response.content),
            {'error_code': -5,
             'error_message': 'Expected parameter title'}
        )

    def test_add_exists(self):
        category_parent = self.create_category('Category')
        category = self.create_category('Subcategory',
                                        parent=category_parent)

        producer = models.Producer.create(
            settings.DEFAULT_LANGUAGE,
            {'title': 'some-producer', 'ethical': True}
        )

        data = {
            "title": "some",
            "info": "vegan",
            "code_type": "barcode",
            "code": "barcode-value",
            "producer_id": producer.id,
            "category_id": category.id
        }
        response = self._post_json('/api/v1/add', data)
        response = self._post_json('/api/v1/add', data)
        self.assertEquals(
            json.loads(response.content),
            {'error_code': -13,
             'error_message': 'Product code already exists'}
        )


    def test_add_photo(self):
        product = self.create_product(codes=[('barcode', 'code'), ])
        photo = SimpleUploadedFile("photo.png", "file_content", content_type="image/png")
        response = self.client.post(
            '/api/v1/add/{}/photo'.format(product.id),
            {'url': photo}
        )
        self.assertTrue(product.get_photo_url())

    def test_add_photo_no_image(self):
        product = self.create_product(codes=[('barcode', 'code'), ])
        response = self.client.post(
            '/api/v1/add/{}/photo'.format(product.id)
        )
        self.assertEquals(
            json.loads(response.content),
            {"error_message": "No image was sent.",
             "error_code": -5}
        )

    def test_add_photo_not_found(self):
        photo = SimpleUploadedFile("photo.png", "file_content", content_type="image/png")
        response = self.client.post(
            '/api/v1/add/999/photo',
            {'url': photo}
        )
        self.assertEquals(
            json.loads(response.content),
            {"error_message": "Product not found.",
             "error_code": -7}
        )

    def test_categories(self):
        self.create_category('Category 1')
        self.create_category('Category 2')
        self.create_category('Category 3')
        response = self.client.get('/api/v1/categories/')
        categories = json.loads(response.content)['result']
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
            json.loads(response.content)['result'],
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

    def test_category_not_found(self):
        response = self.client.get('/api/v1/categories/9999')
        self.assertEquals(
            json.loads(response.content),
            {
                'error_code': -17,
                'error_message': 'Category not found.'
            }
        )

    def test_producers(self):
        p1 = self.create_producer('Producer 1')
        p2 = self.create_producer('Producer 2')
        p3 = self.create_producer('Producer 3')
        p4 = self.create_producer('Some really other producer')
        response = self.client.get('/api/v1/producers/')

        self.assertEquals(
            json.loads(response.content)['result'],
            [{"id": p1.id,
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
              "title": "Some really other producer"}],
        )

        response = self.client.get('/api/v1/producers/', {'title': 'Pro'})
        self.assertEquals(
            json.loads(response.content)['result'],
            [{"id": p1.id,
              "ethical": None,
              "title": "Producer 1"},
             {"id": p2.id,
              "ethical": None,
              "title": "Producer 2"},
             {"id": p3.id,
              "ethical": None,
              "title": "Producer 3"},]
        )

    def test_complain(self):
        product = self.create_product()
        response = self._post_json(
            '/api/v1/{}/complain/'.format(product.id),
            {'message': 'test'}
        )
        self.assertEquals(
            json.loads(response.content),
            {u'error_code': 0, u'error_message': None, 'result': None}
        )
        complains = models.Complain.objects.filter(product=product)
        self.assertEquals(len(complains), 1)
        self.assertEquals(complains[0].message, 'test')

    def test_complain_not_found(self):
        response = self._post_json(
            '/api/v1/999/complain/',
            {'message': 'test'}
        )
        self.assertEquals(
            json.loads(response.content),
            {u'error_code': -7, u'error_message': 'Product code not found.'}
        )

    def test_complain_wo_message(self):
        response = self._post_json('/api/v1/999/complain/', {})
        self.assertEquals(
            json.loads(response.content),
            {u'error_code': -5,
             u'error_message': 'Expected parameter message'}
        )
