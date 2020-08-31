from django import forms
from django.core.validators import MinValueValidator
from .models import CATEGORY_CHOICES, Basket,Product,Order

default_status = CATEGORY_CHOICES[0][0]



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")



class BasketForm(forms.ModelForm):
    class Meta:
        model = Basket
        fields = ['amount']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []