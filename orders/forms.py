from django import forms
from orders.models import Order, Supermarket

class SupermarketForm(forms.ModelForm):
    class Meta:
        model = Supermarket
        fields = "__all__"


class OrdersForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["STATUS_CHOICES, supermarket, "]
    