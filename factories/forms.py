from django import forms
from factories.models import Factory


class FactoryForm(forms.ModelForm):
    class Meta:
        model = Factory
        fields = ["name", "location"]
