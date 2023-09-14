from django.urls import path
from wellcome.views import wellcome

urlpatterns = [
    path('',wellcome, name='wellcome'),
]