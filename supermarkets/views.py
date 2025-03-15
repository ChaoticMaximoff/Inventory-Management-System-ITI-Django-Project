from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.urls import reverse_lazy
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
    fields = ["name", "location"]
    template_name = "supermarkets/supermarket_form.html"
    success_url = reverse_lazy("supermarket_list")


class SupermarketUpdateView(LoginRequiredMixin, UpdateView):
    model = Supermarket
    fields = ["name", "location"]
    template_name = "supermarkets/supermarket_form.html"
    success_url = reverse_lazy("supermarket_list")


class SupermarketDeleteView(LoginRequiredMixin, DeleteView):
    model = Supermarket
    template_name = "supermarkets/supermarket_confirm_delete.html"
    success_url = reverse_lazy("supermarket_list")
