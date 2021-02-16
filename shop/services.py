from django.http import HttpResponseRedirect
from .models import CartProduct
from .utils import CartMixin
from django.views.generic import View
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Sum


class AddProductToCart(CartMixin, View):
    """Добавляет товар в корзину"""

    def get(self, *args, **kwargs):
        ct_model = kwargs.get('ct_model')
        product_slug = kwargs.get('slug')

        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)

        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner,
            cart=self.cart,
            content_type=content_type,
            object_id=product.id,
        )

        cart_product.final_price = cart_product.number * cart_product.content_object.price

        if created:
            self.cart.products.add(cart_product)
        if not self.cart.products:
            self.cart.total_products = 0
            self.cart.final_price = 0

        cart_data = self.cart.products.aggregate(Sum('final_price'), Count('id'))
        if cart_data.get('final_price__sum'):
            self.cart.final_price = cart_data['final_price__sum']
        else:
            self.cart.final_price = 0

        if cart_data.get('id__count'):
            self.cart.total_products = cart_data['id__count']
        else:
            self.cart.total_products = cart_data['id__count']

        cart_product.save()
        self.cart.save()
        return HttpResponseRedirect('/cart/')
