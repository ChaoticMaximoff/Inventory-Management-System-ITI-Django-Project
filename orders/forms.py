from django.utils import timezone
from django import forms
from orders.models import Order, Supermarket, OrderItem

# class SupermarketForm(forms.ModelForm):
#     class Meta:
#         model = Supermarket
#         fields = "__all__"



class OrdersForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["supermarket", "receive_date"]
        widgets = {"receive_date": forms.DateInput(attrs={"type": "date"})}

    def clean_receive_date(self):
        receive_date = self.cleaned_data.get("receive_date")
        if receive_date < timezone.now().date():
            raise forms.ValidationError("Receive date cannot be in the past.")
        return receive_date

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")
        return quantity
    

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields =[ "product", "quantity"]