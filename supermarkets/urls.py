from django.urls import path
from .views import (
    SupermarketListView,
    SupermarketDetailView,
    SupermarketCreateView,
    SupermarketUpdateView,
    SupermarketDeleteView,
)


urlpatterns = [
    path("", SupermarketListView.as_view(), name="supermarket_list"),
    path("<int:pk>/", SupermarketDetailView.as_view(), name="supermarket_detail"),
    path("create/", SupermarketCreateView.as_view(), name="supermarket_create"),
    path("<int:pk>/edit/", SupermarketUpdateView.as_view(), name="supermarket_edit"),
    path(
        "<int:pk>/delete/", SupermarketDeleteView.as_view(), name="supermarket_delete"
    ),
]
