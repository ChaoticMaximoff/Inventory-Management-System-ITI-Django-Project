from django import forms
from shipments.models import Shipment, ShipmentItem


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ["factory", "receive_date"]

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")
        return quantity


class ShipmentItemForm(forms.ModelForm):
    class Meta:
        model = ShipmentItem
        fields = ["product", "quantity"]
