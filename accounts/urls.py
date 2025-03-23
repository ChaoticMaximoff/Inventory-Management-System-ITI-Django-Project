from django.urls import path
from .views import LoginView, RegisterView, index, DashboardView,UserLogoutView
app_name = 'accounts'

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('home/', index, name='index'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]

