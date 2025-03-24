from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
import sweetify
from .models import Order, OrderItem, Supermarket
from django.contrib.auth.mixins import (
    UserPassesTestMixin,
    LoginRequiredMixin,
)  # for permissions
from django.views import View
from django.contrib import messages
from .forms import OrdersForm, OrderItemForm
from django.core.paginator import Paginator
from .filters import OrderFilter
from django.db.models import Case, When, Value, IntegerField


# custom mixin for the required rules
class RoleRequiredMixin(UserPassesTestMixin):
    required_roles = []

    def test_func(self):  # checking if the user has the required roles
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if "EMPLOYEE" in self.required_roles and user.role.upper() == "MANAGER":
            return True

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

        return redirect("orders")


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/order_list.html"
    context_object_name = "orders"
    paginate_by = 8

    def get_queryset(self):
        queryset = Order.objects.annotate(
            status_order=Case(
                When(status="PENDING", then=Value(0)),
                When(status="CONFIRMED", then=Value(1)),
                output_field=IntegerField(),
            )
        ).order_by("status_order", "-created_at")
        self.filterset = OrderFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset
        return context


class OrderDetailsView(DetailView):
    model = Order
    template_name = "orders/order_details.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()

        # Paginate order items
        items_per_page = 5
        paginator = Paginator(order.items.all(), items_per_page)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Add pagination objects to the context
        context["page_obj"] = page_obj
        context["is_paginated"] = page_obj.has_other_pages()
        return context


class OrdersCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = OrdersForm()
        return render(
            request, "orders/order_form.html", {"form": form, "mode": "create"}
        )

    def post(self, request):
        form = OrdersForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by_user = request.user
            order.save()
            sweetify.success(
                request,
                title="Order created",
                icon="success",
                text="Order has been created successfully.",
                timer=3000,
                position="top-end",
                toast=True,
                showConfirmButton=False,
            )
            return redirect("orders")
        sweetify.error(
            request,
            title="Error",
            icon="error",
            text="There was an error creating the order. Please check the form and try again.",
            timer=3000,
            position="top-end",
            toast=True,
            showConfirmButton=False,
        )
        return render(
            request, "orders/order_form.html", {"form": form, "mode": "create"}
        )


class OrderCreateItemView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk, status="PENDING")
        form = OrderItemForm()
        return render(
            request, "orders/order_item_form.html", {"form": form, "order": order}
        )

    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk, status="PENDING")

        form = OrderItemForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data["product"]
            quantity = form.cleaned_data["quantity"]

            if quantity > product.quantity:
                sweetify.error(
                    request,
                    title="Cannot add item",
                    icon="error",
                    text="Quantity exceeds available stock",
                    timer=2000,
                    position="top-end",
                    toast=True,
                    showConfirmButton=False,
                )
                return render(
                    request,
                    "orders/order_item_form.html",
                    {"form": form, "order": order},
                )

            # Decrease the stock of the product
            product.quantity -= quantity
            product.save()

            item = form.save(commit=False)
            item.created_by_user = request.user
            item.order = order
            item.save()

            sweetify.success(
                request,
                title="Item added",
                icon="success",
                text="Item has been added to the order successfully.",
                timer=2000,
                position="top-end",
                toast=True,
                showConfirmButton=False,
            )

            return redirect("order_items", pk=order.id)

        error_message = form.errors.as_text()

        sweetify.error(
            request,
            title="Error",
            icon="error",
            text=f"Failed to add item to order: {error_message}",
            timer=2000,
            position="top-end",
            toast=True,
            showConfirmButton=False,
        )
        return render(
            request, "orders/order_item_form.html", {"form": form, "order": order}
        )


class OrderConfirmView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk, status="PENDING")

        if not order.items.exists():
            sweetify.error(
                request,
                title="Cannot confirm order",
                icon="error",
                text="Cannot confirm an empty order",
                timer=2000,
                position="top-end",
                toast=True,
                showConfirmButton=False,
            )
            return redirect("order_items", pk=order.id)

        order.status = "CONFIRMED"
        order.save()
        sweetify.success(
            self.request,
            title="Order confirmed",
            icon="success",
            text="Stock updated successfully.",
            timer=3000,
            position="top-end",
            toast=True,
            showConfirmButton=False,
        )
        return redirect("order_items", pk=order.id)


class SupermarketOrderListView(ListView):
    model = Order
    template_name = "order/order_detail.html"
    context_object_name = "orders"

    def get_queryset(self):
        supermarket_id = self.kwargs["supermarket_id"]
        return Order.objects.filter(supermarket_id=supermarket_id).order_by(
            "-created_at"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["supermarket"] = Supermarket.objects.get(
            id=self.kwargs["supermarket_id"]
        )
        return context


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrdersForm
    template_name = "orders/order_form.html"
    success_url = reverse_lazy("orders")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mode"] = "update"
        return context

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.status == "CONFIRMED":
            sweetify.error(
                request,
                title="Cannot update order",
                icon="error",
                text="Order is already confirmed",
                timer=2000,
                position="top-end",
                toast=True,
                showConfirmButton=False,
            )
            return redirect("orders")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        sweetify.success(
            self.request,
            title="Order updated",
            icon="success",
            timer=2000,
            position="top-end",
            toast=True,
            showConfirmButton=False,
        )
        return super().form_valid(form)


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy("orders")

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            if self.object.status == "CONFIRMED":
                sweetify.error(
                    request,
                    title="Cannot delete order",
                    icon="error",
                    text="Order is already confirmed",
                    timer=2000,
                    position="top-end",
                    toast=True,
                    showConfirmButton=False,
                )
                return redirect("orders")

            self.object.delete()
            sweetify.success(
                request,
                title="Order deleted",
                icon="success",
                text="Order has been deleted successfully",
                timer=2000,
                position="top-end",
                toast=True,
                showConfirmButton=False,
            )
            return redirect("orders")

        except Exception as e:
            sweetify.error(
                request,
                title="Error deleting order",
                icon="error",
                text=str(e),
                timer=2000,
                position="top-end",
                toast=True,
                showConfirmButton=False,
            )
            return redirect("orders")


class OrderItemDeleteView(LoginRequiredMixin, DeleteView):
    model = OrderItem

    def get_success_url(self):
        return reverse_lazy("order_items", kwargs={"pk": self.object.order.pk})

    def post(self, request, *args, **kwargs):
        orderitem = self.get_object()
        order = orderitem.order

        if order.status == "CONFIRMED":
            sweetify.error(
                request,
                title="Cannot delete item",
                icon="error",
                text="Cannot delete from confirmed order",
                timer=2000,
                position="top-end",
                toast=True,
                showConfirmButton=False,
            )
            return redirect("order_items", pk=order.pk)

        # Increase the stock of the product
        product = orderitem.product
        product.quantity += orderitem.quantity
        product.save()

        orderitem.delete()
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
        return redirect("order_items", pk=order.pk)
