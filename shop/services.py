from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect
from django.views.generic import View

from .models import CartProduct
from .utils import CartMixin, CartProductMixin


class AddProductToCart(CartMixin, View):
    """Добавляет товар в корзину"""

    def get(self, *args, **kwargs):
        ct_model_handler = kwargs.get('ct_model').lower()
        product_slug = kwargs.get('slug')

        NAME_CATEGORY_TO_CONTENT_TYPE = {
            'notebooks': 'notebook',
            'smartphones': 'smartphone',
        }

        if ct_model_handler.endswith('s'):
            ct_model = NAME_CATEGORY_TO_CONTENT_TYPE.get(ct_model_handler)
        else:
            ct_model = kwargs.get('ct_model')

        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)

        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner,
            cart=self.cart,
            content_type=content_type,
            object_id=product.id,
        )

        cart_product.number += 1
        cart_product.final_price = cart_product.number * cart_product.content_object.price
        cart_product.save()

        if created:
            self.cart.products.add(cart_product)
        if not self.cart.products:
            self.cart.total_products = 0
            self.cart.final_price = 0

        cart_data = self.cart.products.aggregate(Sum('final_price'), Count('id'))
        if not cart_data['final_price__sum']:
            cart_data['final_price__sum'] = cart_product.content_object.price

        if cart_data['final_price__sum']:
            self.cart.final_price = cart_data['final_price__sum']
        else:
            self.cart.final_price = 0

        if cart_data['id__count']:
            self.cart.total_products = cart_data['id__count']
        else:
            self.cart.total_products = 0

        self.cart.save()

        return HttpResponseRedirect('/cart/')


class ChangeNumberProducts(CartMixin, CartProductMixin, View):
    """Изменяет количество продуктов в корзине"""

    def post(self, request, *args, **kwargs):
        print(request.POST)

        new_number = request.POST.get('number')

        ct_model = kwargs.get('ct_model')
        product_slug = kwargs.get('slug')

        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)

        cart_product = CartProduct.objects.get(
            user=self.cart.owner,
            cart=self.cart,
            content_type=content_type,
            object_id=product.id,
        )

        cart_product.number = new_number
        cart_product.final_price = new_number * cart_product.content_object.price

        cart_product.save()

        self.cart.save()

        return HttpResponseRedirect('/cart/')


class ClearCart(CartProductMixin, CartMixin, View):
    """Очищает корзину"""

    def get(self, *args, **kwargs):
        for cart_product in self.products:
            self.cart.products.remove(cart_product)
            cart_product.delete()

        self.cart.final_price = 0
        self.cart.total_products = 0
        self.cart.save()

        return HttpResponseRedirect('/cart/')


class ClearDetailCart(CartProductMixin, CartMixin, View):
    """Убирает один продукт из корзины"""

    def get(self, *args, **kwargs):
        ct_model = kwargs.get('ct_model')
        product_slug = kwargs.get('slug')

        for product in self.products:
            if product.content_type.model == ct_model and product.content_object.slug == product_slug:
                product.delete()

                self.cart.final_price -= product.final_price

                if product.number > self.cart.total_products:
                    self.cart.total_products -= 1
                else:
                    self.cart.total_products -= product.number
                self.cart.save()

        return HttpResponseRedirect('/cart/')
