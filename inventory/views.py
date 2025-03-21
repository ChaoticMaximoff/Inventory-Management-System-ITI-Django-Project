from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Product
from django.contrib.auth.decorators import login_required
from .forms import ProductForm

# Create your views here.
@login_required
def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    
    context = {
        'products': products,
        'query': query or ''
    }
    return render(request, 'product_list.html', context)

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

def product_delete(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('inventory:product_list')
    return render(request, 'product_delete.html', {'product': product})