import django_filters
from django import forms
from .models import Order


class OrderFilter(django_filters.FilterSet):
    supermarket = django_filters.CharFilter(
        field_name="supermarket__name",
        lookup_expr="icontains",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search supermarket..."}
        ),
    )
    receive_date = django_filters.DateFilter(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=Order.STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Order
        fields = ["supermarket", "receive_date", "status"]
