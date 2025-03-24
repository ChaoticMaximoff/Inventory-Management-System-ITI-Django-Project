from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
import sweetify
from .models import Product
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
@login_required
def product_list(request):
    query = request.GET.get('q')
    if query:
        products_queryset = Product.objects.filter(name__icontains=query)
    else:
        products_queryset = Product.objects.order_by('-created_at')
    
    # Add pagination
    paginator = Paginator(products_queryset, 5) 
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'query': query or ''
    }
    return render(request, 'product_list.html', context)

@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inventory:product_list')
    else:
        form = ProductForm()
    
    context = {
        'form': form
    }
    return render(request, 'product_create.html', context)


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('inventory:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_update.html', {'product': product, 'form': form})

@login_required	
def product_delete(request, pk):
    product = get_object_or_404(Product, id=pk)
    related_shipments = product.shipment_items.all()
    related_orders = product.order_items.all()
    
    if request.method == 'POST':
        if related_shipments or related_orders:
            sweetify.error(
                request,
                title="Cannot delete product",
                icon="error",
                text="This product is related to a shipment or an order. Delete them first to be able to delete this product.",
                timer=5000,
                position="top-end",
                toast=True,
                showConfirmButton=False,
            )
            return redirect('inventory:product_list')
        
        product.delete()
        return redirect('inventory:product_list')
    return render(request, 'product_delete.html', {'product': product})