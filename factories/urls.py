from django.urls import path
from factories.views import (
    FactoryListView,
    FactoryDetailView,
    FactoryCreateView,
    FactoryUpdateView,
    FactoryDeleteView,
)

urlpatterns = [
    path("", FactoryListView.as_view(), name="factory_list"),
    path("<int:pk>/", FactoryDetailView.as_view(), name="factory_detail"),
    path("create/", FactoryCreateView.as_view(), name="factory_create"),
    path("<int:pk>/edit/", FactoryUpdateView.as_view(), name="factory_edit"),
    path("<int:pk>/delete/", FactoryDeleteView.as_view(), name="factory_delete"),
]
