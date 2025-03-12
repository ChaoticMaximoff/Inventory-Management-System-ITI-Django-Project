from django.urls import path
from .views import OrderListView, OrderDetailsView, SupermarketOrderListView

urlpatterns = [
    path('order/', OrderListView.as_view()),
    path('order/<int:pk>/', OrderDetailsView.as_view(), name='order-detail'),
    path('supermarket/<int:supermarket_id>/orders/', SupermarketOrderListView.as_view(), name='supermarket-order-list')
    ]