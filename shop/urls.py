from django.urls import path
from .views import *

urlpatterns = [
    path('', test_view, name='base'),
    path('product/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail')
]

