from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from .models import ProductInBasket
from django.middleware.csrf import get_token

from common.util.common_functions import get_session_key, get_products_nmb, get_basket_total_price


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def basket_adding(request):

    return_dict = dict()
    session_key = get_session_key(request)
    data = request.POST
    product_id = data.get('product_id')
    nmb = data.get('product_nmb')
    price = data.get('product_price')
    color = data.get('product_color')
    product_name = data.get('product_name')
    product_image = data.get('product_image')

    new_product, created = ProductInBasket.objects.update_or_create(
        session_key=session_key,    product_id=product_id,
                                                 image=product_image,
                                                 color_id=color,product_name=product_name, defaults={"nmb": nmb,"price_per_item":price}
    )


    last_adding_product = list(ProductInBasket.objects.filter(session_key=session_key,is_active=True))
    s_last_adding_product = serializers.serialize('json', last_adding_product)
    return_dict['product_total_nmb'] = get_products_nmb(session_key)
    return_dict['last_adding_product'] = s_last_adding_product
    return_dict['basket_total_price'] = get_basket_total_price(session_key)
    return JsonResponse(return_dict)

def delete_small_basket_position(request):
    return_dict = dict()
    data = request.POST
    session_key = get_session_key(request)

    delete_product = ProductInBasket.objects.filter(session_key=session_key,product_id=data.get('product_id'),color_id=data.get(
        'product_color_id'),is_active=True).delete()
    last_adding_product = list(ProductInBasket.objects.filter(session_key=session_key,is_active=True))
    s_last_adding_product = serializers.serialize('json', last_adding_product)

    nmb_after_delete = ProductInBasket.objects.filter(is_active=True).aggregate(Sum('nmb'))

    return_dict['nmb_after_delete'] = nmb_after_delete['nmb__sum']
    return_dict['last_adding_product'] = s_last_adding_product
    return_dict['basket_total_price'] = get_basket_total_price(session_key)
    return JsonResponse(return_dict)

def delete_big_basket_position(request):
    return_dict = dict()
    data = request.POST
    session_key = get_session_key(request)

    delete_product = ProductInBasket.objects.filter(session_key=session_key, product_id=data.get('product_id'), color_id=data.get(
        'product_color_id'), is_active=True).delete()
    last_adding_product = list(ProductInBasket.objects.filter(session_key=session_key, is_active=True))

    csrf = get_token(request)
    s_last_adding_product = serializers.serialize('json', last_adding_product)
    return_dict['last_adding_product'] = s_last_adding_product
    return_dict['basket_total_price'] = get_basket_total_price(session_key)
    return_dict['csrf'] = csrf
    return JsonResponse(return_dict)


def show_basket(request):
    session_key = get_session_key(request)
    active_ancer = 'basket'
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key,is_active=True)
    if products_in_basket:
        basket_total_price = "%.2f" % float(get_basket_total_price(session_key=get_session_key(request)))
    else:
        basket_total_price = 0
    hidden_small_basket = request.path
    csrf = get_token(request)

    if is_ajax(request=request):
        print('вошли в ajax')
        data = request.POST

        product_id = data.get('product_id')
        nmb = data.get('product_nmb')
        color = data.get('product_color_id')
        updated_product = ProductInBasket.objects.get(color_id=color,session_key=get_session_key(request),product_id=product_id)
        updated_product.nmb = nmb
        updated_product.save()

    return render(request, 'orders/basket.html', locals())

def checkout(request):
    print('checkout')
    if request.POST:
        print('request.POST :', request.POST)
    return render(request, 'orders/checkout.html', locals())


