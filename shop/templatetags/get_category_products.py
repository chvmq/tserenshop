from django.template import Library
from ..models import Notebook, Smartphone

register = Library()


@register.simple_tag()
def get_notebooks():
    return Notebook.objects.all()


@register.simple_tag()
def get_smartphones():
    return Smartphone.objects.all()
