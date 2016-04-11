from django.contrib import admin
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


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Producer, ProducerAdmin)
admin.site.register(models.CodeType)
