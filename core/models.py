from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.utils.html import format_html


INFO_CHOICES = (
    ('vegan', 'vegan'),
    ('vegeterian', 'vegeterian'),
    ('fish', 'fish'),
    ('meat', 'meat'),
)

CODES = (
    ('qrcode', 'QR Code'),
    ('barcode', 'BAR Code')
)

LANGS = (
    ('ru', 'ru'),
    ('en', 'en'),
)


def take_title(objects):
    all = objects.order_by('lang').values_list('lang', 'title')
    for lang, title in all:
        if lang == settings.DEFAULT_LANGUAGE:
            return title

    return None


class Producer(models.Model):
    ethical = models.BooleanField(default=True)

    @staticmethod
    def create(lang, data):
        producer = Producer(ethical=data['ethical'])
        producer.save()
        title = ProducerTitle(
            producer=producer,
            title=data['title'],
            lang=lang
        )
        title.save()

        return producer

    def __unicode__(self):
        title = self.producertitle_set.order_by('lang').first()
        if title:
            return title.title
        else:
            return self.id

    def get_title(self, lang):
        title = self.producertitle_set.filter(lang=lang).first()
        if title:
            return title.title
        else:
            return None

    def get_dict(self, lang):
        return {
            'id': self.id,
            'title': self.get_title(lang),
            'ethical': self.ethical
        }


class ProducerTitle(models.Model):
    producer = models.ForeignKey(Producer)
    lang = models.CharField(max_length=64, choices=LANGS)
    title = models.CharField(max_length=512)


class Category(models.Model):
    parent = models.ForeignKey('Category', null=True, blank=True)

    def __unicode__(self):
        title = self.categorytitle_set.order_by('lang').first()
        if title:
            return title.title
        else:
            return self.id

    def get_title(self, lang):
        title = self.categorytitle_set.filter(lang=lang).first()
        if title:
            return title.title
        else:
            return ''

    def get_json_tree(self, lang):
        tree = {
            'id': self.id,
            'title': self.get_title(lang),
        }
        return tree


class CategoryTitle(models.Model):
    category = models.ForeignKey(Category)
    lang = models.CharField(max_length=64, choices=LANGS)
    title = models.CharField(max_length=512)


class Product(models.Model):
    info = models.CharField(max_length=255, choices=INFO_CHOICES)
    producer = models.ForeignKey(Producer)
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return take_title(self.producttitle_set)

    @staticmethod
    def dict_by_id(product_id, lang):
        product = models.Product.objects.select_related()\
                                        .filter(id=product_id)\
                                        .first()
        return product.to_dict(lang)


    def get_title(self, lang):
        title = self.producttitle_set.filter(lang=lang).first()
        if title:
            return title.title
        else:
            return None

    def get_photo_url(self):
        photo = self.productphoto_set.first()
        if photo:
            return photo.get_url()
        return None

    def to_dict(self, lang):
        result = {
            'id': self.id,
            'title': self.get_title(lang),
            'info': self.info,
            'codes': {code.type: code.code
                      for code in self.productcode_set.all()},
            'photo': self.get_photo_url(),
            'producer': {'id': self.producer.id,
                         'title': self.producer.get_title(lang),
                         'ethical': self.producer.ethical},
        }
        category = self.category.get_json_tree(lang)
        if self.category.parent:
            category_parent = self.category.parent.get_json_tree(lang)
            category_parent['sub'] = category
            result['category'] = category_parent
        else:
            result['category'] = category

        return result



class ProductCode(models.Model):
    product = models.ForeignKey(Product)
    type = models.CharField(max_length=64, choices=CODES)
    code = models.CharField(max_length=512)


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to='static/product',
                              default=None,
                              null=True)

    def get_url(self):
        return settings.PHOTO_HOST + '/' + self.image.url

    def img_tag(self):
        return format_html('<img src="%s"/>' % self.get_url())


class ProductTitle(models.Model):
    product = models.ForeignKey(Product)
    lang = models.CharField(max_length=64, choices=LANGS)
    title = models.CharField(max_length=512)
