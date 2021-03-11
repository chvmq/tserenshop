from django.test import TestCase, RequestFactory

from shop.models import Category, Notebook, Cart
from shop.services import *


class ServiceTestCase(TestCase):
    def setUp(self) -> None:
        self.user = Account.objects.create(username='lari', password='lari')
        self.category = Category.objects.create(title='Notebook', slug='notebook')
        self.notebook = Notebook.objects.create(
            category=self.category,
            title='macOs',
            slug='macos',
            description='cool',
            price='100000',
            diagonal='13',
            display='IPS',
            processor_freq='3.1',
            ram='4',
            video='ryzen5'
        )

        self.notebook_2 = Notebook.objects.create(
            category=self.category,
            title='macair',
            slug='macair',
            description='cool',
            price='50000',
            diagonal='13',
            display='IPS',
            processor_freq='3.1',
            ram='4',
            video='ryzen5'
        )

        self.cart = Cart.objects.create(owner=self.user)

        self.cart_product_notebook_2 = CartProduct.objects.create(
            user=self.user, cart=self.cart, content_object=self.notebook_2,
            final_price='50000'
        )

    def test_print(self):
        print(self.category)
        print(self.user)
        print(self.notebook)
        print(self.notebook_2)
        print(self.cart)

    def test_add_product_in_cart_manually(self):
        self.cart.products.add(self.cart_product_notebook_2)
        self.cart.final_price += int(self.notebook_2.price)
        self.cart.total_products += 1

    def test_add_to_cart(self, ct_model='notebook', slug='macos'):
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user

        response = AddProductToCart.as_view()(request, ct_model=ct_model, slug=slug)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/')

        user_cart = Cart.objects.get(owner=request.user)
        self.assertEqual(str(user_cart), 'Корзина пользователя lari')

        user_products = CartProduct.objects.all()
        self.assertEqual(str(user_products[0]), 'Продукт macair для корзины')
        self.assertEqual(str(user_products[1]), 'Продукт macOs для корзины')

        self.assertEqual(user_cart.total_products, 1)
        self.assertEqual(user_cart.final_price, 100000)

    def test_change_number_product_in_cart(self):
        self.test_add_to_cart()
        factory = RequestFactory()
        request = factory.post(
            'change_num_product/notebook/macos/',
            {'number': '3'}
        )
        request.user = self.user

        response = ChangeNumberProducts.as_view()(request, slug='macos')

        user_cart = Cart.objects.get(owner=request.user)
        self.assertEqual(user_cart.total_products, 1)
        self.assertEqual(user_cart.final_price, 350000)
        user_products = CartProduct.objects.all()
        self.assertEqual(user_products[1].number, 3)

    def test_clear_cart(self):
        self.test_add_to_cart()
        request = RequestFactory().get('/')
        request.user = self.user

        response = ClearCart.as_view()(request)
        self.assertEqual(response.status_code, 302)

        cart_user = Cart.objects.get(owner=request.user)
        self.assertEqual(cart_user.total_products, 0)
        self.assertEqual(cart_user.final_price, 0)

    def test_clear_detail_product_cart(self):
        self.test_add_to_cart()
        # self.test_add_product_in_cart_manually()
        request = RequestFactory().get('/')
        request.user = self.user

        response = ClearDetailCart.as_view()(request, ct_model='notebook', slug='macos')
        self.assertEqual(response.status_code, 302)

        cart_user = Cart.objects.get(owner=request.user)
        print(cart_user.total_products, cart_user.final_price)
        self.assertEqual(cart_user.total_products, 0)
        self.assertEqual(cart_user.final_price, 0)
