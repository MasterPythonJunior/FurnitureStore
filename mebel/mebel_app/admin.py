from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product, Gallery, Size, Order, OrderProduct


#
# Register your models here.
class GalleryInline(admin.TabularInline):
    model = Gallery
    # model = Size
    fk_name = 'product'
    extra = 1
class SizeInline(admin.TabularInline):
    model = Size
    fk_name = 'product'
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'image', 'get_products_count', 'slug']
    list_display_links = ['pk', 'title']
    list_editable = ['image']
    list_filter = ['title']
    prepopulated_fields = {'slug': ('title',)}

    def get_products_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        else:
            return '0'

    get_products_count.short_description = 'Кол-во товаров'


class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'price', 'color', 'quantity', 'category', 'get_photo']
    list_display_links = ['pk', 'title']
    list_editable = ['price', 'color', 'quantity']
    inlines = [GalleryInline, SizeInline]

    prepopulated_fields = {'slug': ('title',)}

    def get_photo(self, obj):
        if obj:
            try:
                return mark_safe(f'<img src="{obj.images.first().photo.url}" width=75 >')
            except:
                return '-'
        else:
            return '-'

    get_photo.short_description = 'Фото'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderProduct)
# admin.site.register(Product)
