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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap class to the supermarket dropdown
        self.fields['supermarket'].widget.attrs.update({'class': 'form-select w-50'})    

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields =[ "product", "quantity"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class': 'form-select w-25'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})