from django.contrib import admin
from products.models import ProductCategory, ProductImage, Product


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductCategory._meta.fields]


    class Meta:
        model = ProductCategory


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Product._meta.fields]
    list_display = ['id','name','short_description','discount','category','price_without_discount','price','is_active','created','updated']
    inlines = [ProductImageInline]



    class Meta:
        model = Product

class ProductImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductImage._meta.fields]

    class Meta:
        model = ProductImage

admin.site.register(ProductImage,ProductImageAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductCategory,ProductCategoryAdmin)
