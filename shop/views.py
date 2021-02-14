from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, View, ListView
from .models import Notebook, Smartphone, Category, LatestProducts, Customer, Cart


def index(request):
    products = LatestProducts.objects.get_products_for_main_page('notebook', 'smartphone')
    customer = Customer.objects.get(user=request.user)
    cart = Cart.objects.get(owner=customer)
    context = {
        'products': products,
        'customer': customer,
        'cart': cart,
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


class CartView(View):
    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        context = {
            'cart': cart,
            'customer': customer,
        }
        return render(request, 'shop/cart.html', context)


class CategoryListView(ListView):
    model = Category
    template_name = 'shop/category_list.html'
    context_object_name = 'category'

    def get_queryset(self):
        return Category.objects.get(slug=self.kwargs['slug'])
