from django.contrib import admin

# from orders.models import Status, Order, ProductInOrder, Color, ProductInBasket
from orders.models import ProductInOrder, Order, Color, Status, ProductInBasket


class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    inlines = [ProductInOrderInline]

    class Meta:
        model = Order


class StatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Status._meta.fields]

    class Meta:
        model = Status

class ColorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Color._meta.fields]

    class Meta:
        model = Color

class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductInOrder._meta.fields]

    class Meta:
        model = ProductInOrder

class ProductInBasketAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductInBasket._meta.fields]

    class Meta:
        model = ProductInBasket

admin.site.register(ProductInBasket,ProductInBasketAdmin)
admin.site.register(ProductInOrder,ProductInOrderAdmin)
admin.site.register(Color,ColorAdmin)

admin.site.register(Order,OrderAdmin)
admin.site.register(Status,StatusAdmin)
