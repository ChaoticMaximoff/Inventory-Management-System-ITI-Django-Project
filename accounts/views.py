from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import LoginForm, RegisterForm
from django.views import generic
import sweetify

class LoginView(generic.View):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('accounts:index')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password, backend='accounts.backends.EmailBackend')
            if user is not None:
                login(request, user)
                return render(request, self.template_name, {'form': form, 'login_success': True})
        return render(request, self.template_name, {'form': form})
    
        
class RegisterView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    def test_func(self):
        return self.request.user.role == "manager"
    
    login_url = ""
    redirect_field_name = "redirect_to"
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:index')

    def form_valid(self, form):
        user = form.save()
        user.backend = 'accounts.backends.EmailBackend'
        login(self.request, user)
        return render(self.request, self.template_name, {'form': form, 'register_success': True})
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

def index(request):        
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'Dashboard.html')