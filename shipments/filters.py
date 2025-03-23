import django_filters
from django import forms
from .models import Shipment


class ShipmentFilter(django_filters.FilterSet):
    factory = django_filters.CharFilter(
        field_name="factory__name",
        lookup_expr="icontains",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search factory..."}
        ),
    )
    receive_date = django_filters.DateFilter(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    confirmed = django_filters.BooleanFilter(
        widget=forms.Select(
            attrs={"class": "form-select"},
            choices=[
                ("", "All"),
                (True, "Yes"),
                (False, "No"),
            ],
        )
    )

    class Meta:
        model = Shipment
        fields = ["factory", "receive_date", "confirmed"]
