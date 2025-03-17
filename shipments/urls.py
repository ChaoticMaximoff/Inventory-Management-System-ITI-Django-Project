from django.urls import path
from shipments.views import (
    ShipmentListView,
    ShipmentDetailView,
    ShipmentCreateView,
    ShipmentItemCreateView,
    ShipmentConfirmView,
)

urlpatterns = [
    path("", ShipmentListView.as_view(), name="shipment_list"),
    path("<int:pk>/", ShipmentDetailView.as_view(), name="shipment_detail"),
    path("create/", ShipmentCreateView.as_view(), name="shipment_create"),
    path(
        "<int:shipment_id>/add-item/",
        ShipmentItemCreateView.as_view(),
        name="shipment_add_item",
    ),
    path(
        "<int:shipment_id>/confirm/",
        ShipmentConfirmView.as_view(),
        name="shipment_confirm",
    ),
]
