from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Order, Supermarket

class OrderListView(ListView):
    model = Order
    template_name= 'order_list.html'
    context_object_name ='orders'

    def get_queryset(self):
        return Order.objects.all().order_by('-created_at') #---> for ordering

 
class OrderDetailsView(DetailView):
    model = Order
    template_name = 'order_details.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class SupermarketOrderListView(ListView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'orders'

def get_queryset(self):
    supermarket_id = self.kwargs['supermarket_id']
    return Order.objects.filter(supermarket_id=supermarket_id).order_by('-created_at')

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['supermarket'] = Supermarket.objects.get(id=self.kwargs['supermarket_id'])
    return context