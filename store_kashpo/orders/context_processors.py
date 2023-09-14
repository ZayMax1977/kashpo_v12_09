from common.util.common_functions import get_session_key, get_products_nmb
from orders.models import ProductInBasket


def get_list_products_in_basket(request):
    session_key = get_session_key(request)
    basket_products_list = ProductInBasket.objects.filter(session_key=session_key, is_active=True)


    products_nmb = get_products_nmb(session_key)

    return locals()

def get_basket_total_price(request):
    session_key = get_session_key(request)
    arr_basket_total_price = ProductInBasket.objects.filter(session_key=session_key, is_active=True).values('total_price')
    basket_total_price = 0
    for i in arr_basket_total_price:
        basket_total_price += i['total_price']

    return locals()

