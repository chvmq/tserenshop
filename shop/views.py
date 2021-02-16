from django.shortcuts import render
from django.views.generic import DetailView, View, ListView
from .models import Notebook, Smartphone, Category, LatestProducts, Customer, Cart
from .utils import *


class IndexView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        products = LatestProducts.objects.get_products_for_main_page(
            'notebook', 'smartphone', with_respect_to='notebook'
        )
        context = {
            'products': products,
            'cart': self.cart
        }
        return render(request, 'shop/index.html', context)


class ProductDetailView(DetailView):
    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        return context

    context_object_name = 'product'
    template_name = 'shop/product_detail.html'
    slug_url_kwarg = 'slug'


class CartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart,
        }
        return render(request, 'shop/cart.html', context)


class CategoryListView(ListView):
    model = Category
    template_name = 'shop/category_list.html'
    context_object_name = 'category'

    def get_queryset(self):
        return Category.objects.get(slug=self.kwargs['slug'])
