from django.template import Library
from ..models import Category

register = Library()


@register.simple_tag()
def get_category_for_sidebar():
    """Получение категорий для сайдбара"""
    return Category.objects.all()


@register.simple_tag()
def get_title_above_sidebar():
    title = 'Товары'
    return title
