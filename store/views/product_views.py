from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from ..models import Product
from ..forms import ProductForm
from ..utils.date_utils import get_product_time


def product_list(request):
    search_term = request.GET.get("search")
    sort_order = request.GET.get("sort")

    products = Product.objects.all()

    if search_term:
        products = products.filter(Q(name__icontains=search_term))

    if sort_order == "ascending":
        products = products.order_by("price")
    elif sort_order == "descending":
        products = products.order_by("-price")

    return render(
        request,
        "product/product_list.html",
        {"products": products},
    )


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    created_tz, updated_tz, created_utc, updated_utc = get_product_time(product)
    context = {
        "product": product,
        "created_tz": created_tz,
        "updated_tz": updated_tz,
        "created_utc": created_utc,
        "updated_utc": updated_utc,
    }

    return render(request, "product/product_detail.html", context)


def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "product/product_form.html", {"form": form})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "product/product_form.html", {"form": form})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(
        request,
        "product/product_confirm_delete.html",
        {"product": product},
    )
