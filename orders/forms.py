from django.utils import timezone
from django import forms
from orders.models import Order, OrderItem


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap class to the supermarket dropdown
        self.fields["supermarket"].widget.attrs.update({"class": "form-select"})
        self.fields["receive_date"].widget.attrs.update({"class": "form-control"})


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity <= 5:
            raise forms.ValidationError("Quantity must be greater than 5.")
        return quantity

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].widget.attrs.update({"class": "form-select"})
        self.fields["quantity"].widget.attrs.update({"class": "form-control"})
