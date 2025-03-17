from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView
from shipments.models import Shipment
from shipments.forms import ShipmentForm, ShipmentItemForm
from django.core.paginator import Paginator


class RoleRequiredMixin(UserPassesTestMixin):
    required_roles = []

    def test_func(self):
        user = self.request.user

        if not user.is_authenticated:
            return False

        # Superusers have all permissions
        if user.is_superuser:
            return True

        # Managers inherit employee permissions
        if "EMPLOYEE" in self.required_roles and user.role.upper() == "MANAGER":
            return True

        return user.role.upper() in [role.upper() for role in self.required_roles]

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("shipment_list")


class ShipmentListView(LoginRequiredMixin, ListView):
    model = Shipment
    template_name = "shipments/shipment_list.html"
    context_object_name = "shipments"
    ordering = ["-created_at"]
    paginate_by = 2

    def get_queryset(self):
        return Shipment.objects.select_related("factory", "created_by")


class ShipmentDetailView(LoginRequiredMixin, DetailView):
    model = Shipment
    template_name = "shipments/shipment_detail.html"
    context_object_name = "shipment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shipment = self.get_object()

        # Paginate shipment items
        items_per_page = 2
        paginator = Paginator(shipment.items.all(), items_per_page)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Add pagination objects to the context
        context["page_obj"] = page_obj
        context["is_paginated"] = page_obj.has_other_pages()
        return context


class ShipmentCreateView(LoginRequiredMixin, RoleRequiredMixin, View):
    required_roles = ["EMPLOYEE"]

    def get(self, request):
        form = ShipmentForm()
        return render(request, "shipments/shipment_form.html", {"form": form})

    def post(self, request):
        form = ShipmentForm(request.POST)
        if form.is_valid():
            shipment = form.save(commit=False)
            shipment.confirmed = False
            shipment.created_by = request.user
            shipment.save()
            messages.success(request, "Shipment created successfully!")
            return redirect("shipment_list")
        return render(request, "shipments/shipment_form.html", {"form": form})


class ShipmentItemCreateView(LoginRequiredMixin, RoleRequiredMixin, View):
    required_roles = ["EMPLOYEE"]

    def get(self, request, shipment_id):
        shipment = get_object_or_404(Shipment, id=shipment_id, confirmed=False)
        form = ShipmentItemForm()
        return render(
            request,
            "shipments/shipment_item_form.html",
            {"form": form, "shipment": shipment},
        )

    def post(self, request, shipment_id):
        shipment = get_object_or_404(Shipment, id=shipment_id, confirmed=False)
        form = ShipmentItemForm(request.POST)
        if form.is_valid():
            shipment_item = form.save(commit=False)
            shipment_item.shipment = shipment
            shipment_item.created_by = request.user
            shipment_item.save()
            messages.success(request, "Item added to shipment!")
            return redirect("shipment_detail", pk=shipment.id)
        return render(
            request,
            "shipments/shipment_item_form.html",
            {"form": form, "shipment": shipment},
        )


class ShipmentConfirmView(LoginRequiredMixin, RoleRequiredMixin, View):
    required_roles = ["MANAGER"]

    def post(self, request, shipment_id):
        shipment = get_object_or_404(Shipment, id=shipment_id, confirmed=False)

        if not shipment.items.exists():
            messages.error(request, "Cannot confirm an empty shipment.")
            return redirect("shipment_detail", pk=shipment.id)

        for item in shipment.items.all():
            product = item.product
            product.quantity += item.quantity
            product.save()

        shipment.confirmed = True
        shipment.save()
        messages.success(request, "Shipment confirmed! Stock updated.")
        return redirect("shipment_detail", pk=shipment.id)
