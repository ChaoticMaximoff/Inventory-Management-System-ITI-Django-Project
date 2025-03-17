from django.urls import path
from .views import OrderListView, OrderDetailsView, SupermarketOrderListView, OrdersCreateView

urlpatterns = [
    path('', OrderListView.as_view()),
    path('order/<int:pk>/', OrderDetailsView.as_view(), name='order-detail'),
    path('supermarket/<int:supermarket_id>/orders/', SupermarketOrderListView.as_view(), name='supermarket-order-list'),
    path('create/', OrdersCreateView.as_view(), name='order_create'),
    ]