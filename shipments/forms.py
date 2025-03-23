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

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")
        return quantity
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['factory'].widget.attrs.update({'class': 'form-select w-25'})
        self.fields['receive_date'].widget.attrs.update({'class': 'form-select'})




class ShipmentItemForm(forms.ModelForm):
    class Meta:
        model = ShipmentItem
        fields = ["product", "quantity"]
        
    def __init___(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class': 'form-select w-25'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})


