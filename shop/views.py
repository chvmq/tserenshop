from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Notebook, Smartphone


def test_view(request):
    print(request)
    return HttpResponse('hello world')


class ProductDetailView(DetailView):

    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)


    # model = Model
    # queryset = Model.objects.all()
    context_object_name = 'product'
    template_name = 'shop/product_detail.html'
    slug_url_kwarg = 'slug'
