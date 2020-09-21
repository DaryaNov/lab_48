from django.urls import path, include

from webapp.views.views import IndexView, ProductView, ProductCreateView, \
    ProductUpdateView, ProductDeleteView

from webapp.views.order_view import BasketView, BasketAddView, \
    BasketDeleteView, BasketDeleteOneView, OrderCreateView


app_name = 'webapp'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('product/', include([
        path('add/', ProductCreateView.as_view(), name='product_create'),
        path('<int:pk>/', include([
            path('', ProductView.as_view(), name='product_view'),
            path('update/', ProductUpdateView.as_view(), name='product_update'),
            path('delete/', ProductDeleteView.as_view(), name='product_delete'),
            path('add-to-basket/', BasketAddView.as_view(), name='product_add_to_basket'),
        ])),
    ])),

    path('cart/', include([
        path('', BasketView.as_view(), name='basket_view'),
        path('<int:pk>/', include([
            path('delete/', BasketDeleteView.as_view(), name='basket_delete'),
            path('delete-one/', BasketDeleteOneView.as_view(), name='basket_delete_one'),
        ])),
    ])),

    path('order/create/', OrderCreateView.as_view(), name='order_create'),
]
