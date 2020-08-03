from django import forms
from django.core.validators import MinValueValidator
from .models import CATEGORY_CHOICES

default_status = CATEGORY_CHOICES[0][0]




class ProductForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, initial='name', label='Название')
    price = forms.DecimalField(max_digits=7, decimal_places=2,label='Цена', initial='price')
    amount = forms.IntegerField(initial='amount',label='Остаток')
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, initial=default_status, label='Категория')
    description = forms.CharField(max_length=2000, required=True,  initial='description', label='Описание')