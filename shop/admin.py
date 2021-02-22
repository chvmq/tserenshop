from django.contrib import admin
from .models import *
from django.forms import ModelChoiceField


class NotebookAdminForm(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebook'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    prepopulated_fields = {'slug': ['title']}


class SmartphoneAdminForm(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphone'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    prepopulated_fields = {'slug': ['title']}


class CategoryAdminForm(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}


admin.site.register(Category, CategoryAdminForm)
admin.site.register(Notebook, NotebookAdminForm)
admin.site.register(Smartphone, SmartphoneAdminForm)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Order)
