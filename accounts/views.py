from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
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
        else:
            error_message = " ".join(form.non_field_errors())
            if error_message:
                sweetify.error(
                    request,
                    'Error',
                    text=error_message,
                    toast=True,
                    position='top',
                    timer=3000,
                    timerProgressBar=True,
                    showConfirmButton=False,
                )
        return render(request, self.template_name, {'form': form})
    
        
class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:index')

    def form_valid(self, form):
        user = form.save()
        user.backend = 'accounts.backends.EmailBackend'
        login(self.request, user)
        return render(self.request, self.template_name, {'form': form, 'register_success': True})
    
    def form_invalid(self, form):
        error_message = " ".join([error for errors in form.errors.values() for error in errors])
        if error_message:
            sweetify.error(self.request, 'Error', text=error_message, toast=True, position='top', timer=3000, timerProgressBar=True, showConfirmButton=False)
        return self.render_to_response(self.get_context_data(form=form))

def index(request):        
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'Dashboard.html')