from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
import sweetify
from factories.models import Factory
from django.contrib.auth.mixins import LoginRequiredMixin


class FactoryListView(LoginRequiredMixin, ListView):
    model = Factory
    template_name = "factories/factory_list.html"
    context_object_name = "factories"
    paginate_by = 5


class FactoryDetailView(LoginRequiredMixin, DetailView):
    model = Factory
    template_name = "factories/factory_detail.html"


class FactoryCreateView(LoginRequiredMixin, CreateView):
    model = Factory
    fields = ["name", "location"]
    template_name = "factories/factory_form.html"
    success_url = reverse_lazy("factory_list")


class FactoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Factory
    fields = ["name", "location"]
    template_name = "factories/factory_form.html"
    success_url = reverse_lazy("factory_list")


class FactoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Factory
    template_name = "factories/factory_confirm_delete.html"
    success_url = reverse_lazy("factory_list")
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.shipments.exists():
            sweetify.error(
                request,
                title="Cannot delete factory",
                icon="error",
                text="This factory is related to a shipment or multiple shipments. Delete them first to be able to delete this factory.",
                timer=5000,
                position="top-end",
                toast=True,
                showConfirmButton=False,
            )
            return redirect("factory_list")
        return super().dispatch(request, *args, **kwargs)
