from django.contrib import admin
from django.utils.html import format_html
from products.models import Category, Image, Product, Subcategory


class CategoryAdmin(admin.ModelAdmin):
    def change_button(self, obj):
        return format_html('<a class="btn" href="/admin/products/category/{}'
                           '/change/">Изменить</a>', obj.id)

    def delete_button(self, obj):
        return format_html('<a class="btn" href="/admin/products/category/{}'
                           '/delete/">Удалить</a>', obj.id)

    list_display = ('id', 'name', 'slug', 'change_button', 'delete_button',)


class SubcategoryAdmin(admin.ModelAdmin):
    def change_button(self, obj):
        return format_html('<a class="btn" href="/admin/products'
                           '/subcategory/{}/change/">Изменить</a>', obj.id)

    def delete_button(self, obj):
        return format_html('<a class="btn" href="/admin/products'
                           '/subcategory/{}/delete/">Удалить</a>', obj.id)

    list_display = ('id', 'category', 'name', 'slug',
                    'change_button', 'delete_button',)


class ProductAdmin(admin.ModelAdmin):
    def change_button(self, obj):
        return format_html('<a class="btn" href="/admin/products'
                           '/product/{}/change/">Изменить</a>', obj.id)

    def delete_button(self, obj):
        return format_html('<a class="btn" href="/admin/products'
                           '/product/{}/delete/">Удалить</a>', obj.id)

    list_display = ('id', 'subcategory', 'name', 'slug', 'price',
                    'change_button', 'delete_button',)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'product',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Image, ImageAdmin)
