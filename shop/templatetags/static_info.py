from django.template import Library

menu = [
    {'title': 'About', 'url_name': 'index'},
    {'title': 'Contact', 'url_name': 'index'},
    {'title': 'Card', 'url_name': 'cart'},
]

register = Library()


@register.simple_tag()
def get_static_info():
    return menu
