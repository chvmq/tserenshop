from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Order


class UserLoginForm(AuthenticationForm):
    """Логин"""
    username = forms.CharField(
        label='username',
        widget=forms.TextInput(attrs={"class": 'form-control'}))

    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs={"class": 'form-control'}))

    class Meta:
        fields = (
            'username', 'password'
        )


class UserRegisterForm(UserCreationForm):
    """Регистрация"""
    username = forms.CharField(
        label='username',
        widget=forms.TextInput(attrs={"class": 'form-control'})
    )

    password1 = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs={"class": 'form-control'})
    )

    password2 = forms.CharField(
        label='confirm password',
        widget=forms.PasswordInput(attrs={"class": 'form-control'})
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={"class": 'form-control'})
    )

    class Meta:
        model = get_user_model()
        fields = (
            'username', 'password1', 'password2', 'email'
        )


class OrderForm(forms.ModelForm):
    """Форма заказа"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата получения заказа'
        print(locals())

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 4, 'rows': 5}))

    class Meta:
        model = Order
        fields = (
            'first_name',
            'last_name',
            'phone',
            'address',
            'buying_type',
            'order_date',
            'comment',
        )
