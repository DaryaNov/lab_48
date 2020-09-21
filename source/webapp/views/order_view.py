from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView

from webapp.forms import BasketForm, OrderForm
from webapp.models import Basket, Product, Order, OrderProduct


class BasketView(ListView):
    # model = Cart
    template_name = 'order/order_view.html'
    context_object_name = 'basket'

    # вместо model = Cart
    # для выполнения запроса в базу через модель
    # вместо подсчёта total-ов в Python-е.
    def get_queryset(self):
        return Basket.get_with_product().filter(pk__in=self.get_basket_ids())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['basket_total'] = Basket.get_basket_total(ids=self.get_basket_ids())
        context['form'] = OrderForm()
        return context

    def get_basket_ids(self):
        basket_ids = self.request.session.get('basket_ids', [])
        print(basket_ids)
        return self.request.session.get('basket_ids', [])


class BasketAddView(CreateView):
    model = Basket
    form_class = BasketForm

    def post(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # qty = 1
        # бонус
        qty = form.cleaned_data.get('qty', 1)

        try:
            basket_product = Basket.objects.get(product=self.product, pk__in=self.get_basket_ids())
            basket_product.amount += qty
            if basket_product.amount <= self.product.amount:
                basket_product.save()
        except Basket.DoesNotExist:
            if qty <= self.product.amount:
                basket_product = Basket.objects.create(product=self.product, qty=qty)
                self.save_to_session(basket_product)

        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return redirect(self.get_success_url())

    def get_success_url(self):
        # бонус
        next = self.request.GET.get('next')
        if next:
            return next
        return reverse('webapp:index')

    def get_basket_ids(self):
        return self.request.session.get('basket_ids', [])

    def save_to_session(self, basket_product):
        basket_ids = self.request.session.get('basket_ids', [])
        if basket_product.pk not in basket_ids:
            basket_ids.append(basket_product.pk)
        self.request.session['basket_ids'] = basket_ids


class BasketDeleteView(DeleteView):
    model = Basket
    success_url = reverse_lazy('webapp:basket_view')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.delete_from_session()
        self.object.delete()
        return redirect(success_url)

    def delete_from_session(self):
        basket_ids = self.request.session.get('basket_ids', [])
        basket_ids.remove(self.object.pk)
        self.request.session['basket_ids'] = basket_ids

    # удаление без подтверждения
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


# бонус
class BasketDeleteOneView(BasketDeleteView):
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        self.object.qty -= 1
        if self.object.qty < 1:
            self.delete_from_session()
            self.object.delete()
        else:
            self.object.save()

        return redirect(success_url)


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('webapp:index')

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     order = self.object
    #     # неоптимально: на каждый товар в корзине идёт 3 запроса:
    #     # * добавить товар в заказ
    #     # * обновить остаток товара
    #     # * удалить товар из корзины
    #     for item in Cart.objects.all():
    #         product = item.product
    #         qty = item.qty
    #         order.order_products.create(product=product, qty=qty)
    #         product.amount -= qty
    #         product.save()
    #         item.delete()
    #     return response

    def form_valid(self, form):
        response = super().form_valid(form)
        order = self.object
        # оптимально:
        # цикл сам ничего не создаёт, не обновляет, не удаляет
        # цикл работает только с объектами в памяти
        # и заполняет два списка: products и order_products
        basket_products = Basket.objects.all()
        products = []
        order_products = []
        for item in basket_products:
            product = item.product
            amount = item.amount
            product.amount -= amount
            products.append(product)
            order_product = OrderProduct(order=order, product=product, amount=amount)
            order_products.append(order_product)
        # массовое создание всех товаров в заказе
        OrderProduct.objects.bulk_create(order_products)
        # массовое обновление остатка у всех товаров
        Product.objects.bulk_update(products, ('amount',))
        # массовое удаление всех товаров в корзине
        basket_products.delete()
        return response

    def form_invalid(self, form):
        return redirect('webapp:basket_view')
