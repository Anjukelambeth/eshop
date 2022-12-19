from django.contrib import admin

from accounts.models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulate_fields = { 'product_slug':('product_name',)}
admin.site.register(Product,ProductAdmin)