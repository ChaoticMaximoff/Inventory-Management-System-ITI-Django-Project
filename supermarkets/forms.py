from django import forms
from supermarkets.models import Supermarket


class SupermarketForm(forms.ModelForm):
    class Meta:
        model = Supermarket
        fields = ["name", "location"]
