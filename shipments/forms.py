from django import forms
from shipments.models import Shipment, ShipmentItem


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ["factory", "receive_date"]


class ShipmentItemForm(forms.ModelForm):
    class Meta:
        model = ShipmentItem
        fields = ["product", "quantity"]
