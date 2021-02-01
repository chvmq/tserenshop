from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

TABLE_HEAD = '''
<table class="table">
    <tbody>
'''
TABLE_FOOT = '''
    </tbody>
</table>
'''

TABLE_CONTENT = '''
    <tr>
        <td>{name}</td>
        <td>{value}</td>
    </tr>
'''

PRODUCT_SPEC = {
    'notebook':
        {
            'Диагональ': 'diagonal',
            'Дисплей': 'display',
            'Частота процессора': 'processor_freq',
            'ОЗУ': 'ram',
            'Видеокарта': 'video',
        },
    'smartphone':
        {
            'Диагональ': 'diagonal',
            'ОЗУ': 'ram',
            'Камера': 'camera',
            'Фронтальная камера': 'front_camera',
            'Баттарея': 'battery',
        }
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content

@register.simple_tag
def product_spec(product):
    model_name = product.__class__._meta.model_name
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_FOOT)
