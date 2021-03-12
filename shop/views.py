from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .forms import OrderForm, UserRegisterForm, UserLoginForm
from .models import Notebook, Smartphone, Category, LatestProducts
from .utils import *


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'SUCCESS')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'FAIL')
    else:
        form = UserRegisterForm()

    return render(request, 'shop/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'SUCCESS')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'FAIL')
            return HttpResponseRedirect('/')
    else:
        form = UserLoginForm()

    return render(request, 'shop/login.html', {'form': form})


def user_logout(request):
    messages.success(request, 'YOU HAVE LOGOUTED')
    logout(request)
    return HttpResponseRedirect('/')


class IndexView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        products = LatestProducts.objects.get_products_for_main_page(
            'notebook', 'smartphone', with_respect_to='notebook'
        )
        context = {
            'products': products,
            'cart': self.cart,
            'number_products_in_cart': self.cart.total_products,
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


class CategoryListView(CartMixin, ListView):
    model = Category
    template_name = 'shop/category_list.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context

    def get_queryset(self):
        return Category.objects.get(slug=self.kwargs['slug'])


class CheckOutView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'form': form,
        }
        return render(request, 'shop/checkout.html', context)
