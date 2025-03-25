from django import forms
from factories.models import Factory


class FactoryForm(forms.ModelForm):
    class Meta:
        model = Factory
        fields = ["name", "location"]
        widgets = { 
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap classes to all fields
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
