from django import forms
from django.utils import timezone
from shipments.models import Shipment, ShipmentItem


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ["factory", "receive_date"]
        widgets = {"receive_date": forms.DateInput(attrs={"type": "date"})}

    def clean_receive_date(self):
        receive_date = self.cleaned_data.get("receive_date")
        if receive_date < timezone.now().date():
            raise forms.ValidationError("Receive date cannot be in the past.")
        return receive_date

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["factory"].widget.attrs.update({"class": "form-select"})
        self.fields["receive_date"].widget.attrs.update({"class": "form-control"})


class ShipmentItemForm(forms.ModelForm):
    class Meta:
        model = ShipmentItem
        fields = ["product", "quantity"]
        widgets = {
            "product": forms.Select(attrs={"class": "form-select w-25 form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
        }
    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity <= 5:
            raise forms.ValidationError("Quantity must be greater than 5.")
        return quantity

    def __init___(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].widget.attrs.update({"class": "form-select w-25"})
        self.fields["quantity"].widget.attrs.update({"class": "form-control"})
