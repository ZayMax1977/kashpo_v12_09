from django.urls import path

# from products.views import  product
from products.views import product

urlpatterns = [
    path('<int:product_id>', product, name='product'),

]