from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import LoginForm, RegisterForm
from django.views import generic
from inventory.models import Product
from django.db.models import Count, Sum, Q, F, OuterRef, Subquery
from orders.models import Order, OrderItem, OrderItem, Supermarket
from shipments.models import Shipment
import sweetify
from datetime import timedelta
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.core.paginator import Paginator  

class LoginView(generic.View):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('accounts:dashboard')

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.role == "manager":
                return redirect('accounts:dashboard')
            else:
                return redirect('inventory:product_list')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            if request.user.role == "manager":
                return redirect('accounts:dashboard')
            else:
                return redirect('inventory:product_list')
                
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password, backend='accounts.backends.EmailBackend')
            if user is not None:
                login(request, user)
                if user.role == "manager":
                    return redirect('accounts:dashboard')
                else:
                    return redirect('inventory:product_list')
        return render(request, self.template_name, {'form': form})
@method_decorator(never_cache, name='dispatch')  # Apply to dispatch method
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

class RegisterView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    def test_func(self):
        return self.request.user.role == "manager"
    
    login_url = ""
    redirect_field_name = "redirect_to"
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:dashboard')

    def form_valid(self, form):
        user = form.save()
        user.backend = 'accounts.backends.EmailBackend'
        login(self.request, user)
        return render(self.request, self.template_name, {'form': form, 'register_success': True})
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

def index(request):        
    return render(request, 'index.html')

@method_decorator(never_cache, name='get')  # Apply to get method
class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'Dashboard.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = Product.objects.annotate(order_item_count=Count('order_items')).order_by('-order_item_count')
        paginator = Paginator(products, 4)  # 4 products per page
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        # Fetch low-stock products (quantity < critical_level)
        low_stock_products = Product.objects.filter(
            quantity__lt=F('critical_level')
        ).select_related().annotate(
            # Get the most recent OrderItem's related Order's Supermarket
            latest_supermarket=Subquery(
                OrderItem.objects.filter(
                    product=OuterRef('pk')
                ).order_by('-order__created_at').values('order__supermarket__name')[:1]
            )
        )
        
        # Fetch orders for total orders and status counts
        orders = Order.objects.all()
        
        # Fetch order items with related data for the other table
        order_items = OrderItem.objects.select_related('product', 'order', 'created_by_user', 'order__supermarket')
        
        total_order_items = order_items.count()
        
        # Total Products
        total_products = products.count()

        # Total orders
        total_orders = orders.count()
        
        # Order status counts (case-insensitive for flexibility)
        order_status_counts = orders.aggregate(
            pending=Count('id', filter=Q(status__iexact=Order.PENDING)),
            confirmed=Count('id', filter=Q(status__iexact=Order.CONFIRMED)),
        )
        
        # Total quantity ordered per product
        product_order_totals = OrderItem.objects.values('product__name').annotate(
            total_ordered=Sum('quantity')
        )
        
        # Orders per supermarket
        supermarket_order_counts = Order.objects.values('supermarket__name').annotate(
            order_count=Count('id')
        )







# --- Sales & Purchase Data (Last 7 Days) ---
        today = timezone.now().date()
        week_start = today - timedelta(days=6)  # Last 7 days
        days = [week_start + timedelta(days=i) for i in range(7)]
        labels = [day.strftime('%a') for day in days]  # e.g., Mon, Tue, etc.

        # Sales: Total quantity ordered per day (confirmed orders)
        sales_data = (
            OrderItem.objects.filter(
                order__status='CONFIRMED',
                order__created_at__gte=week_start,  # Direct DateTimeField comparison
                order__created_at__lte=today + timedelta(days=1)  # Include all of today
            )
            .annotate(day=TruncDate('order__created_at'))
            .values('day')
            .annotate(total_quantity=Sum('quantity'))
            .order_by('day')
        )
        sales_dict = {entry['day']: entry['total_quantity'] for entry in sales_data}
        sales = [sales_dict.get(day, 0) for day in days]

        # Purchases: Total quantity ordered per day (pending orders)
        purchase_data = (
            OrderItem.objects.filter(
                order__status='PENDING',
                order__created_at__gte=week_start,  # Direct DateTimeField comparison
                order__created_at__lte=today + timedelta(days=1)  # Include all of today
            )
            .annotate(day=TruncDate('order__created_at'))
            .values('day')
            .annotate(total_quantity=Sum('quantity'))
            .order_by('day')
        )
        purchase_dict = {entry['day']: entry['total_quantity'] for entry in purchase_data}
        purchases = [purchase_dict.get(day, 0) for day in days]

        # --- Stock Chart Data ---
        quantity_in_hand = Product.objects.aggregate(total=Sum('quantity'))['total'] or 0
        to_be_received = (
            OrderItem.objects.filter(order__status='PENDING')
            .aggregate(total=Sum('quantity'))['total'] or 0
        )









        # Populate context
        context['products'] = page_obj
        context['total_products'] = total_products
        context['low_stock_products'] = low_stock_products  # For Stock Alert table
        context['orders'] = orders
        context['order_items'] = order_items
        context['total_order_items'] = total_order_items
        context['total_orders'] = total_orders
        context['new_orders'] = order_status_counts['pending']
        context['delivered_orders'] = order_status_counts['confirmed']
        context['order_status_counts'] = order_status_counts
        context['product_order_totals'] = product_order_totals
        context['supermarket_order_counts'] = supermarket_order_counts
        context['supermarkets'] = Supermarket.objects.all()
        


# From your DashboardView
        context['chart_labels'] = labels  # e.g., ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        context['sales_data'] = sales  # e.g., [0, 0, 10, 0, 0, 0, 0]
        context['purchase_data'] = purchases  # e.g., [0, 0, 5, 0, 0, 0, 0]
        context['quantity_in_hand'] = quantity_in_hand
        context['to_be_received'] = to_be_received

        # For the table
        print("Chart Labels:", labels)
        print("Sales Data:", sales)
        print("Purchase Data:", purchases)





        return context