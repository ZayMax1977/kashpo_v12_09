from django.shortcuts import render

from products.models import ProductImage


def home(request):
    products_images = ProductImage.objects.filter(is_active=True,is_main=True, product__is_active = True)
    products_images_kashpo = products_images.filter(product__category_id = 1)
    products_images_stoyka = products_images.filter(product__category_id = 2)
    products_images_furniture = products_images.filter(product__category_id = 3)
    active_ancer = 'home'

    return render(request,'home/home.html', locals())
