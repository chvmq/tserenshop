from django.template import Library

menu = [
    {'title': 'About', 'url_name': 'index'},
    {'title': 'Contact', 'url_name': 'index'},
    {'title': 'Sign up', 'url_name': 'register'},
    {'title': 'Sign in', 'url_name': 'login'},
    {'title': 'Log out', 'url_name': 'logout'},
]

register = Library()


@register.simple_tag()
def get_static_info():
    return menu
