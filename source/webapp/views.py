from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.http import HttpResponseNotAllowed, Http404
from django.views import View
from webapp.models import Product, Basket,Order
from webapp.forms import ProductForm,SimpleSearchForm,BasketForm,OrderForm
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView,ListView,TemplateView
from .base import SearchView
from django.urls import reverse,reverse_lazy


class IndexView(SearchView):
    template_name = 'index.html'
    context_object_name = 'products'
    paginate_by = 5
    paginate_orphans = 0
    model = Product
    search_fields = ['name__icontains']

    def get_queryset(self):
        data = super().get_queryset()
        return data

class ProductView(TemplateView):
    template_name = 'product_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=pk)

        context['product'] = product
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_create.html'

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product_update.html'
    form_class = ProductForm

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    template_name = 'product_delete.html'
    model = Product
    success_url = reverse_lazy('index')

# ======================================================


class BasketCreateView(CreateView):
    model = Basket
    template_name = 'basket_view.html'
    form_class = BasketForm

    def form_valid(self, form):
        totals = {}
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        for products in product:
            if products not in totals:
                totals[products] = 0
            totals[products] += 1
        totals = form.save(commit=False)
        totals.product = product
        totals.save()
        return redirect('product_view',pk=product.pk)



class BasketView(TemplateView):
    template_name = 'basket_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        product = get_object_or_404(Basket, pk=pk)

        context['product'] = product
        return context

# =================================================================

class OrderCreateView(CreateView):
    model = Order
    template_name = 'order_create.html'
    form_class = OrderForm

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        order = form.save(commit=False)
        order.product = product
        order.save()
        form.save_m2m()
        return redirect('order_view', pk=product.pk)


class OrderView(TemplateView):
    template_name = 'order_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        order = get_object_or_404(Order, pk=pk)

        context['order'] = order
        return context
