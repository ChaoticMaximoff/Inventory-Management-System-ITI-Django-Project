from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control rounded-pill py-3 px-5',
                'id': 'email',
                'placeholder': 'Enter your Email',
                'required': True
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control rounded-pill py-3 px-5',
                'id': 'password',
                'placeholder': 'Password',
                'required': True
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()
            if not user:
                raise forms.ValidationError("User with this email does not exist.")
            if not user.check_password(password):
                raise forms.ValidationError("Invalid password.")
        return cleaned_data

class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        label='Role',
        widget=forms.Select(attrs={'class': 'form-control rounded-pill py-3 px-5', 'id': 'role', 'required': True})
    )
    username = forms.CharField(
        label='User Name',
        widget=forms.TextInput(attrs={'class': 'form-control rounded-pill py-3 px-5', 'id': 'username', 'placeholder': 'User Name', 'required': True})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control rounded-pill py-3 px-5', 'id': 'email', 'placeholder': 'Email', 'required': True})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control rounded-pill py-3 px-5', 'id': 'password', 'placeholder': 'Password', 'required': True})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control rounded-pill py-3 px-5', 'id': 'password2', 'placeholder': 'Confirm Password', 'required': True})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with this username already exists.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user