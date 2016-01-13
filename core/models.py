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
