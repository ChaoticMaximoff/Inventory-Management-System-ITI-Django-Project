from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from shipments.models import Shipment, ShipmentItem
from shipments.forms import ShipmentForm, ShipmentItemForm
from django.core.paginator import Paginator
import sweetify
from .filters import ShipmentFilter
from .forms import ShipmentItemForm


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
        sweetify.error(
            self.request,
            title="Permission denied",
            icon="error",
            text="You do not have the permission to access this page.",
            timer=3000,
            position="top-end",
            toast=True,
            showConfirmButton=False,
        )
        return redirect("shipment_list")


class ShipmentListView(LoginRequiredMixin, ListView):
    model = Shipment
    template_name = "shipments/shipment_list.html"
    context_object_name = "shipments"
    paginate_by = 8

    def get_queryset(self):
        queryset = Shipment.objects.order_by("confirmed")
        self.filterset = ShipmentFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset
        return context


class ShipmentDetailView(LoginRequiredMixin, DetailView):
    model = Shipment
    template_name = "shipments/shipment_detail.html"
    context_object_name = "shipment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shipment = self.get_object()

        # Paginate shipment items
        items_per_page = 8
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
        return render(
            request, "shipments/shipment_form.html", {"form": form, "mode": "create"}
        )

    def post(self, request):
        form = ShipmentForm(request.POST)
        if form.is_valid():
            shipment = form.save(commit=False)
            shipment.confirmed = False
            shipment.created_by = request.user
            shipment.save()
            sweetify.success(
                request,
                title="Success",
                icon="success",
                text="Shipment created successfully",
                timer=2000,
                position="top-end",
                toast=True,
                showConfirmButton=False,
            )
            return redirect("shipment_list")

        # Capture the specific error message
        error_message = form.errors.as_text()

        sweetify.error(
            request,
            title="Error",
            icon="error",
            text=f"Failed to create shipment: {error_message}",
            timer=2000,
            position="top-end",
            toast=True,
            showConfirmButton=False,
        )
        return render(
            request, "shipments/shipment_form.html", {"form": form, "mode": "create"}
        )


class ShipmentItemCreateView(LoginRequiredMixin, RoleRequiredMixin, View):
    required_roles = ["EMPLOYEE"]
    form_class = ShipmentItemForm

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

            sweetify.success(
                request,
                title="Success",
                icon="success",
                text="Item added to shipment successfully",
                timer=2000,
                position="top-end",
                toast=True,
                showConfirmButton=False,
            )
            return redirect("shipment_detail", pk=shipment.id)

        # Capture the specific error message
        error_message = form.errors.as_text()

        sweetify.error(
            request,
            title="Error",
            icon="error",
            text=f"Failed to add item to shipment: {error_message}",
            timer=2000,
            position="top-end",
            toast=True,
            showConfirmButton=False,
        )
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
            sweetify.error(
                request,
                title="Cannot confirm shipment",
                icon="error",
                text="Cannot confirm an empty shipment",
                timer=2000,
                showConfirmButton=True,
            )
            return redirect("shipment_detail", pk=shipment.id)

        try:
            for item in shipment.items.all():
                product = item.product
                product.quantity += item.quantity
                product.save()

            shipment.confirmed = True
            shipment.save()

            sweetify.success(
                request,
                title="Success",
                icon="success",
                text="Shipment confirmed and stock updated",
                timer=2000,
                position="top-end",
                toast=True,
                showConfirmButton=False,
            )
        except Exception as e:
            sweetify.error(
                request,
                title="Error confirming shipment",
                icon="error",
                text=str(e),
                timer=2000,
                position="top-end",
                toast=True,
                showConfirmButton=False,
            )

        return redirect("shipment_detail", pk=shipment.id)


class ShipmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Shipment
    form_class = ShipmentForm
    template_name = "shipments/shipment_form.html"
    success_url = reverse_lazy("shipment_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add mode to context to differentiate between create and update
        context["mode"] = "update"
        return context

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.confirmed:
            sweetify.error(
                request,
                title="Cannot update shipment",
                icon="error",
                text="Shipment is already confirmed",
                timer=2000,
                position="top-end",
                toast=True,
                showConfirmButton=False,
            )
            return redirect("shipment_detail", pk=self.object.pk)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        sweetify.success(
            self.request,
            title="Success",
            icon="success",
            text="Shipment updated successfully",
            timer=2000,
            position="top-end",
            toast=True,
            showConfirmButton=False,
        )
        return response


class ShipmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Shipment
    success_url = reverse_lazy("shipment_list")

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            if self.object.confirmed:
                sweetify.error(
                    request,
                    title="Cannot delete shipment",
                    icon="error",
                    text="Shipment is already confirmed",
                    timer=2000,
                    position="top-end",
                    toast=True,
                    showConfirmButton=False,
                )
                return redirect("shipment_list")

            self.object.delete()
            sweetify.success(
                request,
                title="Success",
                icon="success",
                text="Shipment deleted successfully",
                timer=2000,
                position="top-end",
                toast=True,
                showConfirmButton=False,
            )
            return redirect("shipment_list")
        except Exception as e:
            sweetify.error(
                request,
                title="Error",
                icon="error",
                text=str(e),
                timer=2000,
                position="top-end",
                toast=True,
                showConfirmButton=False,
            )
            return redirect("shipment_list")


class ShipmentItemDeleteView(LoginRequiredMixin, DeleteView):
    model = ShipmentItem

    def get_success_url(self):
        return reverse_lazy("shipment_detail", kwargs={"pk": self.object.shipment.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        shipment = self.object.shipment

        if shipment.confirmed:
            sweetify.error(
                request,
                title="Cannot delete item",
                icon="error",
                text="Cannot delete from confirmed shipment",
                timer=2000,
                position="top-end",
                toast=True,
                showConfirmButton=False,
            )
            return redirect("shipment_detail", pk=shipment.pk)

        self.object.delete()
        sweetify.success(
            request,
            title="Success",
            icon="success",
            text="Item removed successfully",
            timer=2000,
            position="top-end",
            toast=True,
            showConfirmButton=False,
        )
        return redirect("shipment_detail", pk=shipment.pk)
