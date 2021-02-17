from django.urls import path
from .views import *
from .services import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('product/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryListView.as_view(), name='category_list'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add_to_cart/<str:ct_model>/<str:slug>/', AddProductToCart.as_view(), name='add_to_cart'),
    path('clear_cart/', ClearCart.as_view(), name='clear_cart'),
    path('clear_detail_cart/<str:ct_model>/<str:slug>/', ClearDetailCart.as_view(), name='clear_detail_cart'),
    path('change_num_product/<str:ct_model>/<str:slug>/', ChangeNumberProducts.as_view(),
         name='change_number_products'),
]
