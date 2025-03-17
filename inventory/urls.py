from django.urls import path
from . import views
app_name = 'inventory'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('create/', views.CreateProductView.as_view(), name='product_create'),
]