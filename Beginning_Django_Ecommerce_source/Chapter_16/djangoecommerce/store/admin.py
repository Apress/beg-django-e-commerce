from django.contrib import admin
from store.models import Product, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    exclude = ('created_at', 'updated_at')

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    exclude = ('created_at', 'updated_at')

admin.site.register(Product, ProductAdmin)
