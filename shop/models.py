from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse


def get_product_url(obj, viewname):
    ct_model = obj.__class__.__name__.lower()
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class LatestProductsManager:
    def get_products_for_main_page(self, *args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)

        for ct_model in ct_models:
            models_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(models_products)

        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to),
                                  reverse=True)

        return products


class LatestProducts:
    objects = LatestProductsManager()


class Category(models.Model):
    title = models.CharField(verbose_name='Категория', max_length=255)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('category_list', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Категория(ю)'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=255, verbose_name='Название')
    price = models.PositiveIntegerField(verbose_name='Цена')
    slug = models.SlugField(verbose_name='Слаг', unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Фото')

    # content_object = GenericRelation

    def __str__(self):
        return self.title


class Notebook(Product):
    class Meta:
        db_table = 'notebook'
        verbose_name = 'Ноутбук'
        verbose_name_plural = 'Ноутбуки'

    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display = models.CharField(max_length=255, verbose_name='Тип дисплея')
    processor_freq = models.CharField(max_length=255, verbose_name='Частота процессора')
    ram = models.CharField(max_length=10, verbose_name='ОЗУ')
    video = models.CharField(max_length=255, verbose_name='Видеокарта')

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

    def __str__(self):
        return f'{self.category.title} {self.title}'


class Smartphone(Product):
    class Meta:
        db_table = 'smartphone'
        verbose_name = 'Смартфон'
        verbose_name_plural = 'Смартфоны'

    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    ram = models.CharField(max_length=10, verbose_name='ОЗУ')
    camera = models.CharField(max_length=255, verbose_name='Камера')
    front_camera = models.CharField(max_length=255, verbose_name='Фронтальная камера')
    battery = models.CharField(max_length=255, verbose_name='Баттарея')
    sd = models.BooleanField(verbose_name='Карта памяти')
    sd_volume = models.CharField(max_length=255, verbose_name='Максимальный объём', blank=True, null=True)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

    def __str__(self):
        return f'{self.category.title} {self.title}'


class CartProduct(models.Model):
    user = models.ForeignKey('account.Account', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveSmallIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    number = models.PositiveIntegerField(default=0, verbose_name='Общее число товаров')
    final_price = models.PositiveIntegerField('Общая цена товаров', null=True)

    def __str__(self):
        return f'Продукт {self.content_object.title} для корзины'

    def get_model_name(self):
        return self.content_type.model


class Cart(models.Model):
    owner = models.ForeignKey('account.Account', verbose_name='Владелец', on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveSmallIntegerField(default=0)
    final_price = models.PositiveIntegerField(default=0)
    in_order = models.BooleanField(verbose_name='В заказе', default=False)
    for_anonymous_user = models.BooleanField(default=False, verbose_name='Для анонимного пользователя')

    def __str__(self):
        return f'{self.owner.username}'
