from django.urls import path
from . import views
app_name = 'inventory'
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('create/', views.create_product, name='product_create'),
    path('update/<int:pk>/', views.product_update, name='product_update'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
]