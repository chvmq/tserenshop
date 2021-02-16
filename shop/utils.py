from django.views.generic import View
from .models import Customer, Cart, CartProduct


class CartProductMixin(View):
    """Возвращает список карт продуктов"""

    def dispatch(self, request, *args, **kwargs):
        products = CartProduct.objects.filter(cart=request.user.id)

        self.products = products
        return super().dispatch(request, *args, **kwargs)


class CartMixin(View):
    """Возвращает корзину"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user
                )
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)

        self.cart = cart

        return super().dispatch(request, *args, **kwargs)
