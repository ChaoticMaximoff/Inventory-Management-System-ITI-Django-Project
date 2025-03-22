from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import LoginView, RegisterView, index, dashboard
app_name = 'accounts'

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
]

