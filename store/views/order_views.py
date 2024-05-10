from django.shortcuts import render, get_object_or_404, redirect
from ..models import Order, Product
from ..forms import OrderForm
from ..decorators import employee_required


@employee_required
def order_list(request):
    orders = Order.objects.all()
    return render(
        request,
        "order/order_list.html",
        {"orders": orders},
    )


@employee_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(
        request,
        "order/order_detail.html",
        {"order": order},
    )


def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            selected_products = request.POST.getlist("products")
            product_quantities = {}

            total_price = 0
            for product_id in selected_products:
                product = Product.objects.get(pk=product_id)
                quantity = int(request.POST.get(f"quantity_{product_id}", 0))

                product.quantity -= quantity
                product.save()

                product_quantities[product_id] = quantity
                total_price += product.price * quantity

            order = form.save(commit=False)
            order.total_price = total_price
            order.save()
            order.products.add(*selected_products)
            order.product_quantities = product_quantities
            order.save()

            return redirect("order_list")
    else:
        form = OrderForm()
    all_products = Product.objects.all()

    context = {"form": form, "all_products": all_products}
    return render(request, "order/order_form.html", context)


@employee_required
def order_update(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)  # Update existing order
        if form.is_valid():
            selected_products = request.POST.getlist("products")
            product_quantities = {}
            current_product_quantities = order.product_quantities

            for product_id, product_quantity in current_product_quantities.items():
                product = Product.objects.get(pk=product_id)
                product.quantity += product_quantity
                product.save()

            total_price = 0
            for product_id in selected_products:
                product = Product.objects.get(pk=product_id)
                quantity = int(request.POST.get(f"quantity_{product_id}", 0))

                product.quantity -= quantity
                product.save()

                product_quantities[product_id] = quantity
                total_price += product.price * quantity

            order.total_price = total_price
            order.products.clear()
            order.products.add(*selected_products)
            order.product_quantities = product_quantities
            order.save()

            return redirect("order_list")
    else:
        initial_data = {
            "employee": order.employee,
            "client": order.client,
        }
        form = OrderForm(initial=initial_data, instance=order)

    all_products = Product.objects.all()
    context = {"form": form, "all_products": all_products}
    return render(request, "order/order_form.html", context)


@employee_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        return redirect("order_list")
    return render(
        request,
        "order/order_confirm_delete.html",
        {"order": order},
    )
