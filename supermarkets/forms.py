from django import forms
from supermarkets.models import Supermarket


class SupermarketForm(forms.ModelForm):
    class Meta:
        model = Supermarket
        fields = ["name", "location"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap classes to all fields
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
