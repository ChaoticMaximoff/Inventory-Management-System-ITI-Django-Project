from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Order, Supermarket
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin #for permissions
from django.views import View
from django.contrib import messages
from .forms import OrdersForm

#custom mixin for the requireed rules
class RoleRequiredMixin(UserPassesTestMixin):
    requied_roles = []
    def test_func(self): #checking if the user has the required roles
        user = self.request.user
        if not user.is_authentcated:
            return False
        if user.is_superuser:
            return True
        if 'EMPOLYEE' in self.requied_roles and user.role.upper():
            return True
    def handle_no_permission(self):
        messages.error(self.request, "You do not have the permission to acces this page.")
        return redirect("../../order_list.html")

class OrderListView(ListView):
    model = Order
    template_name= 'order_list.html'
    context_object_name ='orders'
    #ordering = ["-created_at"]
    #paginate_by = 2

    def get_queryset(self):
        return Order.objects.all().order_by('-created_at') #---> for ordering

 
class OrderDetailsView(DetailView):
    model = Order
    template_name = 'order_details.html'
    context_object_name = 'orders'

    # def get_context_data(self, **kwargs):
    #     return super().get_context_data(**kwargs)

class OrdersCreateView(LoginRequiredMixin, RoleRequiredMixin, View):
    requied_roles=["EMPLOYEE"] #any emplyee can create an order
    def get(self, request):
        form = OrdersForm()
        return render(request, "order_form.html", {"form":form})

    def post(self, request):
        form = OrdersForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            return redirect("order_list.html")
        return render(request, "order_form.html", {"form":form})
            

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