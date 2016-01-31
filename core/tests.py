import json
from django.test import TestCase
from django.test import Client
from django.conf import settings
import models

class ApiBase(TestCase):

    def setUp(self):
        self.client = Client()

    def _post_json(self, url, data):
        return self.client.post(url,
                               json.dumps(data),
                               content_type="application/json")


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
        cases = [
            ({}, expected_err, 400),
            ({'code': '123'}, expected_err, 400),
            ({'type': 'barcode'}, expected_err, 400),
            ({'code': 'unknown', 'type': 'barcode'}, not_found_err, 404),
            #({'code': 'unknown', 'type': 'barcode'}, {}, 200),
        ]
        for args, expected_err, expected_code in cases:
            response = self.client.get('/api/v1/check', args)
            self.assertEquals(
                json.loads(response.content),
                expected_err
            )
            self.assertEquals(response.status_code, expected_code)

    def test_add_producer(self):
        data = {
            "title": "Some good",
            "ethical": True
        }
        response = self._post_json('/api/v1/add-producer', data)

        self.assertEquals(
            json.loads(response.content),
            {"ethical": True, "id": 1, "title": "Some good"}
        )

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
