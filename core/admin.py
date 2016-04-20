from django.contrib import admin
from django.core import urlresolvers

import core.models as models


class CategoryTitleInline(admin.TabularInline):
    model = models.CategoryTitle
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryTitleInline]
    list_filter = 'parent',


class ProductTitleInline(admin.TabularInline):
    model = models.ProductTitle
    extra = 0


class ProductPhotoInline(admin.TabularInline):
    model = models.ProductPhoto
    readonly_fields = 'img_tag',
    extra = 0


class ProductCodeInline(admin.TabularInline):
    model = models.ProductCode
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    search_fields = 'producttitle__title',
    list_filter = 'info', 'category'
    readonly_fields = 'id',
    inlines = [ProductCodeInline,
               ProductTitleInline,
               ProductPhotoInline]
    fieldsets = (
        (None, {
            'fields': ('id', 'category', 'info', 'producer', )
        })
    ),


class ProducerTitle(admin.TabularInline):
    model = models.ProducerTitle
    extra = 0


class ProducerAdmin(admin.ModelAdmin):
    inlines = [ProducerTitle]
    list_filter = 'ethical',


class ComplainAdmin(admin.ModelAdmin):
    list_filter = 'lang', 'status'

    readonly_fields = 'link_to_product',
    fieldsets = (
        (None, {
            'fields': ('lang', 'link_to_product', 'status', 'message', )
        })
    ),

    def link_to_product(self, obj):
        link = urlresolvers.reverse("admin:core_product_change", args=[obj.product.id])
        return u'<a href="%s">%s</a>' % (link, obj.product)
    link_to_product.allow_tags = True


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Producer, ProducerAdmin)
admin.site.register(models.Complain, ComplainAdmin)
admin.site.register(models.CodeType)
