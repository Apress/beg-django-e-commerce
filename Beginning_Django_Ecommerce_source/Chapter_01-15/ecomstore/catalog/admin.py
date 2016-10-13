from django.contrib import admin
from ecomstore.catalog.models import Product, Category, ProductReview
from ecomstore.catalog.forms import ProductAdminForm

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    # sets values for how the admin site lists your products 
    list_display = ('name', 'price', 'old_price', 'created_at', 'updated_at',)
    # which of the fields in 'list_display' tuple link to admin product page
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['-created_at']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    exclude = ('created_at', 'updated_at',)
    # sets up slug to be generated from product name
    prepopulated_fields = {'slug' : ('name',)}
    
# registers your product model with the admin site
admin.site.register(Product, ProductAdmin)
    
class CategoryAdmin(admin.ModelAdmin):
    #sets up values for how admin site lists categories
    list_display = ('name', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    exclude = ('created_at', 'updated_at',)
    
    # sets up slug to be generated from category name
    prepopulated_fields = {'slug' : ('name',)}
    
admin.site.register(Category, CategoryAdmin)

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'title', 'date', 'rating', 'is_approved')
    list_per_page = 20
    list_filter = ('product', 'user', 'is_approved')
    ordering = ['date']
    search_fields = ['user','content','title']
    
admin.site.register(ProductReview, ProductReviewAdmin)
    
    
