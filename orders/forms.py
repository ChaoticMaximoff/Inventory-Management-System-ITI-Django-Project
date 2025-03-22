from django import forms
from orders.models import Order, Supermarket, OrderItem

# class SupermarketForm(forms.ModelForm):
#     class Meta:
#         model = Supermarket
#         fields = "__all__"



class OrdersForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["supermarket"]
    

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields =[ "product", "quantity"]