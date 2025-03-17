from django.urls import path
from shipments.views import (
    ShipmentListView,
    ShipmentDetailView,
    ShipmentCreateView,
    ShipmentItemCreateView,
    ShipmentConfirmView,
    ShipmentUpdateView,  
    ShipmentDeleteView, 
    ShipmentItemDeleteView
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
        "<int:pk>/delete-item",
        ShipmentItemDeleteView.as_view(),
        name="shipment_delete_item",
    ),
    path(
        "<int:shipment_id>/confirm/",
        ShipmentConfirmView.as_view(),
        name="shipment_confirm",
    ),
    path("<int:pk>/edit/", ShipmentUpdateView.as_view(), name="shipment_edit"),
    path("<int:pk>/delete/", ShipmentDeleteView.as_view(), name="shipment_delete"),
]
