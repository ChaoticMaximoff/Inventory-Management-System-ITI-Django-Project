from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Order, Supermarket
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin #for permissions
from django.views import View
from django.contrib import messages
from .forms import OrdersForm, OrderItemForm
from django.core.paginator import Paginator


#custom mixin for the required rules
class RoleRequiredMixin(UserPassesTestMixin):
    required_roles = []
    def test_func(self): #checking if the user has the required roles
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if 'EMPLOYEE' in self.required_roles and user.role.upper() == 'MANAGER':
            return True
    def handle_no_permission(self):
        messages.error(self.request, "You do not have the permission to access this page.")
        return redirect("orders")

class OrderListView(ListView):
    model = Order
    template_name= 'orders/order_list.html'
    context_object_name ='orders'
    ordering = ["-created_at"]
    paginate_by = 8

    def get_queryset(self):
        return Order.objects.all().order_by('-created_at') #---> for ordering

 
class OrderDetailsView(DetailView):
    model = Order
    template_name = 'orders/order_details.html'
    context_object_name = 'order_items'
    ordering = ["-created_at"]



    def get_queryset(self):
        return Order.objects.all().order_by('-created_at') #---> for ordering

    

class OrdersCreateView(LoginRequiredMixin, View):
    #required_roles=["EMPLOYEE"] #any employee can create an order
    def get(self, request):
        form = OrdersForm()
        return render(request, "orders/order_form.html", {"form":form})

    def post(self, request):
        form = OrdersForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by_user = request.user
            order.save()
            return redirect("orders")
        return render(request, "orders/order_form.html", {"form":form})

class OrderCreateItemView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        form = OrderItemForm()
        return render(request, "orders/order_item_form.html", {"form":form, "order":order})
    
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        form = OrderItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by_user = request.user
            item.order = order
            
            if item.quantity <= item.product.quantity and item.product.quantity <= 0:
                item.product.quantity -=item.quantity
                item.product.save()
                item.save()
                return redirect("./")
            else: 
                messages.error(self.request, "NOT ENOUGH STOCK")
                return redirect("./")
        return render(request, "order/order_item_form.html", {"form":form, "order":order})
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
            
class OrderConfirmView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk, status='PENDING')

        if not order.items.exists():
            messages.error(request, "Cannot confirm an empty order.")
            return redirect("orders", pk=order.id)


        order.status = 'CONFIRMED'
        order.save()
        messages.success(request, "order confirmed! Stock updated.")
        return redirect("order_items", pk=order.id)


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