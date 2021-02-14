from django.urls import path
from .views import *
from .services import *

urlpatterns = [
    path('', index, name='index'),
    path('product/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add_to_cart/<str:ct_model>/<str:slug>/', AddProductToCart, name='add_to_cart'),

]
