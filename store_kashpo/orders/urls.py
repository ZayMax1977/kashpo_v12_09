from django.urls import path


from orders.views import basket_adding, delete_small_basket_position, delete_big_basket_position, show_basket, checkout

urlpatterns = [
    path('', basket_adding, name='basket_adding'),
    path('delete_position/', delete_small_basket_position, name='delete_small_basket_position'),
    path('delete_position_basket/', delete_big_basket_position, name='delete_big_basket_position'),
    path('basket/', show_basket, name='show_basket'),
    path('checkout/', checkout, name='checkout'),

]