from celery import shared_task
from .models import Cart, CartProduct


@shared_task
def delete_cart_for_anonymous_user() -> None:
    anonymous_cart = Cart.objects.get(
        for_anonymous_user=True
    )
    anonymous_cart.delete()
