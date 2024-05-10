from django.shortcuts import render, get_object_or_404, redirect
from ..models import TypeOfProduct
from ..forms import TypeOfProductForm


def type_of_product_list(request):
    types_of_products = TypeOfProduct.objects.all()
    return render(
        request,
        "type_of_product/type_of_product_list.html",
        {"types_of_products": types_of_products},
    )


def type_of_product_detail(request, pk):
    type_of_product = get_object_or_404(TypeOfProduct, pk=pk)
    return render(
        request,
        "type_of_product/type_of_product_detail.html",
        {"type_of_product": type_of_product},
    )


def type_of_product_create(request):
    if request.method == "POST":
        form = TypeOfProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("type_of_product_list")
    else:
        form = TypeOfProductForm()
    return render(request, "type_of_product/type_of_product_form.html", {"form": form})


def type_of_product_update(request, pk):
    type_of_product = get_object_or_404(TypeOfProduct, pk=pk)
    if request.method == "POST":
        form = TypeOfProductForm(request.POST, instance=type_of_product)
        if form.is_valid():
            form.save()
            return redirect("type_of_product_list")
    else:
        form = TypeOfProductForm(instance=type_of_product)
    return render(request, "type_of_product/type_of_product_form.html", {"form": form})


def type_of_product_delete(request, pk):
    type_of_product = get_object_or_404(TypeOfProduct, pk=pk)
    if request.method == "POST":
        type_of_product.delete()
        return redirect("type_of_product_list")
    return render(
        request,
        "type_of_product/type_of_product_confirm_delete.html",
        {"type_of_product": type_of_product},
    )
