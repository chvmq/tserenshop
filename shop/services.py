from django.http import HttpResponseRedirect
from .models import Customer, Cart, CartProduct
from django.contrib.contenttypes.models import ContentType


def AddProductToCart(request, *args, **kwargs):
    """Добавляет товар в корзину"""
    ct_model = kwargs.get('ct_model')
    product_slug = kwargs.get('slug')
    customer = Customer.objects.get(user=request.user)
    cart = Cart.objects.get(owner=customer, in_order=False)
    content_type = ContentType.objects.get(model=ct_model)
    product = content_type.model_class().objects.get(slug=product_slug)
    cart_product, created = CartProduct.objects.get_or_create(
        user=cart.owner,
        cart=cart,
        content_type=content_type,
        object_id=product.id,
    )
    if created:
        cart.products.add(cart_product)

    return HttpResponseRedirect('/cart/')
