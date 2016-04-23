# coding: utf-8
import os
import urllib
import csv
import logging

from django.conf import settings
from django.core.files import File
from grab.spider import Spider, Task
import core.models as models


class GoodsMatrixSpider(Spider):
    site = 'http://www.goodsmatrix.ru/'
    initial_urls = ['http://www.goodsmatrix.ru/GoodsCatalogue.aspx']
    s_code = '//span[@id="ctl00_ContentPH_BarCodeL"]'
    s_gname = '//span[@id="ctl00_ContentPH_GoodsName"]'
    s_compo = '//span[@id="ctl00_ContentPH_Composition"]'
    s_category = '//span[@id="ctl00_ContentPH_GroupPath_GroupName"]'
    s_img = '//img[@id="ctl00_ContentPH_LSGoodPicture_GoodImg"]'

    def prepare(self):
        self.visited = set()
        self.code_type, _ = models.CodeType.objects.get_or_create(
            name='EAN13'
        )
        self.producer, _ = models.Producer.get_or_create('ru', 'Неизвестный')


    def task_initial(self, grab, task):
        return self.task_page(grab, task)

    def task_image(self, grab, task):
        path = 'static/product/' + task.img_name
        grab.response.save(
            os.path.join(settings.BASE_DIR, path)
        )
        product_photo = models.ProductPhoto(product=task.product)
        product_photo.image = path
        product_photo.save()

    def task_page(self, grab, task):

        for elem in grab.doc.select('//a'):
            href = elem.node().get('href')
            if href and href.startswith(self.site) and \
               href not in self.visited:
                self.visited.add(href)
                yield Task('page', url=href)


        for elem in grab.doc.select(self.s_code):
            code = elem.text()
            compo = ''

            for elem in grab.doc.select(self.s_gname):
                title = elem.text()

            for elem in grab.doc.select(self.s_compo):
                compo = elem.text()

            for elem in grab.doc.select(self.s_category):
                clist = elem.text().split(' / ')
                category1 = clist[1].strip()
                category2 = clist[2].replace('/', '').strip()

            c1, _ = models.Category.get_or_create(
                lang='ru', title=category1
            )
            c2, _ = models.Category.get_or_create(
                lang='ru', title=category2
            )
            if not c2.parent:
                c2.parent = c1
                c2.save()

            code_obj = models.ProductCode.objects.filter(
                type=self.code_type,
                code=code
            ).first()
            if not code_obj:
                product_obj = models.Product.create(
                    lang='ru',
                    title=title,
                    info='unknown',
                    code_type=self.code_type,
                    code=code,
                    composition=compo,
                    producer=self.producer,
                    category=c2,
                    source='goodsmatrix.ru'
                )

                for elem in grab.doc.select(self.s_img):
                    img_src = elem.node().get('src')
                    yield Task('image',
                               url=self.site + img_src,
                               product=product_obj,
                               img_name=img_src.split('/')[-1])
