from django.db.models import Sum

from orders.models import ProductInBasket


def get_products_nmb(session_key):
    basket_products_nmb = ProductInBasket.objects.filter(session_key=session_key, is_active=True).values('nmb')


    resultdict = {}
    for dictionary in basket_products_nmb:
        for key in dictionary:
            try:
                resultdict[key] += dictionary[key]
            except KeyError:
                resultdict[key] = dictionary[key]

    if len(basket_products_nmb) == 0:
        products_nmb = '0'
    else:
        products_nmb = resultdict['nmb']
    return products_nmb

def get_session_key(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    return session_key

def delete_similar_product_in_basket(product_id,color,nmb):
    similar_product = ProductInBasket.objects.filter(product_id=product_id, color=color,is_active=True)
    similar_product_nmb = similar_product.values('nmb')

    if similar_product_nmb:
        nmb = int(nmb) + similar_product_nmb[0]['nmb']
        similar_product[0].delete()
        return nmb
    return

def get_basket_total_price(session_key):

    basket_total_price = ProductInBasket.objects.filter(session_key=session_key,is_active=True).aggregate(Sum("total_price"))

    return basket_total_price['total_price__sum']