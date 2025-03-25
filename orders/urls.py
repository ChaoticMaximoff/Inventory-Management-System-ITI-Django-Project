from django.urls import path
from .views import (OrderDeleteView, OrderItemDeleteView,
                    OrderListView,
                    OrderDetailsView, OrderUpdateView, 
                    SupermarketOrderListView, 
                    OrdersCreateView, 
                    OrderCreateItemView, 
                    OrderConfirmView)

urlpatterns = [
    path('', OrderListView.as_view(), name='orders'),
    path('create/', OrdersCreateView.as_view(), name='order_create'),
    path('<int:pk>/', OrderDetailsView.as_view(), name='order_items'),
    path('<int:pk>/additem', OrderCreateItemView.as_view(), name='order_add_item'),
    path('<int:pk>/confirm', OrderConfirmView.as_view(), name='order-confirm'),
    path('<int:pk>/delete', OrderDeleteView.as_view(), name='order-delete'),
    path('<int:pk>/update', OrderUpdateView.as_view(), name='order-update'),
    path('<int:pk>/delete-tem', OrderItemDeleteView.as_view(), name='order-item-delete'),
    path('supermarket/<int:supermarket_id>/orders/', SupermarketOrderListView.as_view(), name='supermarket-order-list'),
    ]