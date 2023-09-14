from django.db import models
from django.template.defaultfilters import truncatechars


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Product(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)

    @property
    def short_description(self):
        return truncatechars(self.description, 20)

    discount = models.IntegerField(default=0)
    category = models.ForeignKey(ProductCategory,blank=True, null=True, default=None,on_delete=models.CASCADE)
    price_without_discount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f'{self.name}, id:{self.id}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def save(self, *args, **kwargs):
        if self.discount > 0 and self.price_without_discount == self.price:
            self.price = self.price - (self.price/100 * self.discount)
        super(Product, self).save(*args, **kwargs)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True, default=None,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_photo/%Y/%m/%d/')
    is_main = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'