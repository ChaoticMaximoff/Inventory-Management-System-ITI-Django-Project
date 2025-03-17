from django.urls import path
from .views import OrderListView, OrderDetailsView, SupermarketOrderListView, OrdersCreateView, OrderCreateItemView

urlpatterns = [
    path('', OrderListView.as_view(), name='orders'),
    path('create/', OrdersCreateView.as_view(), name='order_create'),
    path('<int:pk>/', OrderDetailsView.as_view(), name='order_items'),
    path('<int:pk>/additem', OrderCreateItemView.as_view(), name='order-item'),
    path('supermarket/<int:supermarket_id>/orders/', SupermarketOrderListView.as_view(), name='supermarket-order-list'),
    ]