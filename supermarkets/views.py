from django.shortcuts import redirect, render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.urls import reverse_lazy
import sweetify
from supermarkets.forms import SupermarketForm
from supermarkets.models import Supermarket
from django.contrib.auth.mixins import LoginRequiredMixin


class SupermarketListView(LoginRequiredMixin, ListView):
    model = Supermarket
    template_name = "supermarkets/supermarket_list.html"
    context_object_name = "supermarkets"
    paginate_by = 5


class SupermarketDetailView(LoginRequiredMixin, DetailView):
    model = Supermarket
    template_name = "supermarkets/supermarket_detail.html"
    context_object_name = "supermarket"


class SupermarketCreateView(LoginRequiredMixin, CreateView):
    model = Supermarket
    form_class = SupermarketForm
    template_name = "supermarkets/supermarket_form.html"
    success_url = reverse_lazy("supermarket_list")


class SupermarketUpdateView(LoginRequiredMixin, UpdateView):
    model = Supermarket
    form_class = SupermarketForm
    template_name = "supermarkets/supermarket_form.html"
    success_url = reverse_lazy("supermarket_list")


class SupermarketDeleteView(LoginRequiredMixin, DeleteView):
    model = Supermarket
    template_name = "supermarkets/supermarket_confirm_delete.html"
    success_url = reverse_lazy("supermarket_list")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.orders.exists():
            sweetify.error(
                request,
                title="Cannot delete supermarket",
                icon="error",
                text="This supermarket is related to an order or multiple orders. Delete them first to be able to delete this supermarket.",
                timer=5000,
                position="top-end",
                toast=True,
                showConfirmButton=False,
            )
            return redirect("supermarket_list")
        return super().dispatch(request, *args, **kwargs)
