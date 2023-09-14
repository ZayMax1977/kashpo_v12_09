from django.db import models
from django.db.models import SET_NULL

from django.db.models.signals import post_save

from products.models import Product


class Status(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f'Статус {self.name}'

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы Заказа'

class Order(models.Model):
    customer_email = models.EmailField(blank=True,null=True,default=None)
    customer_name = models.CharField(max_length=64,blank=True,null=True,default=None)
    customer_phone = models.CharField(max_length=48, blank=True, null=True, default=None)

    total_price = models.DecimalField(default=0,max_digits=10,decimal_places=2)
    customer_address = models.CharField(max_length=128, blank=True, null=True, default=None)

    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    comments = models.TextField(blank=True,null=True,default=None)
    created = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)

    def __str__(self):
        return f'Заказ ID: {self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class Color(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None)

    def __str__(self):
        return f'Цвет {self.name}'

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

class ProductInBasket(models.Model):
    session_key = models.CharField(max_length=128,blank=True, null=True, default=None)
    order = models.ForeignKey(Order,blank=True, null=True, default=None,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, default=None,on_delete=SET_NULL)
    product_name = models.CharField(max_length=64,blank=True, null=True, default=None)
    nmb = models.IntegerField(default=1)
    color = models.ForeignKey(Color, blank=True, null=True, default=None,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_photo/%Y/%m/%d/',default=None)
    price_per_item = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    total_price = models.DecimalField(default=0,max_digits=10, decimal_places=2) # price_per_item * nmb

    # price_per_item = models.FloatField(default=0)
    # total_price = models.FloatField(default=0) # price_per_item * nmb
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


    def __str__(self):
        return f'{self.product.name}'

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):

        self.price_per_item = self.product.price
        self.total_price = int(self.nmb) * self.price_per_item
        super(ProductInBasket, self).save(*args, **kwargs)

class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, blank=True, null=True, default=None, on_delete=models.CASCADE)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(default=0,max_digits=10,decimal_places=2)
    total_price = models.DecimalField(default=0,max_digits=10,decimal_places=2)

    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)

    def __str__(self):
        return f'Товар в заказе: {self.product.name} {self.product.id}, '

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def save(self, *args, **kwargs):
        self.price_per_item = self.product.price
        self.total_price = self.nmb * self.price_per_item
        super(ProductInOrder, self).save(*args, **kwargs)

def product_in_order_post_save(sender, instance,created,**kwargs):
    order = instance.order

    all_products_in_order = ProductInOrder.objects.filter(order=order,is_active=True)
    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price
    instance.order.total_price = order_total_price
    instance.order.save(force_update=True)

post_save.connect(product_in_order_post_save,sender=ProductInOrder)