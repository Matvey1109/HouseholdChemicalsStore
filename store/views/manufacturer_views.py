from django.shortcuts import render, get_object_or_404, redirect
from ..models import Manufacturer
from ..forms import ManufacturerForm


def manufacturer_list(request):
    manufacturers = Manufacturer.objects.all()
    return render(
        request,
        "manufacturer/manufacturer_list.html",
        {"manufacturers": manufacturers},
    )


def manufacturer_detail(request, pk):
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    return render(
        request,
        "manufacturer/manufacturer_detail.html",
        {"manufacturer": manufacturer},
    )


def manufacturer_create(request):
    if request.method == "POST":
        form = ManufacturerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("manufacturer_list")
    else:
        form = ManufacturerForm()
    return render(request, "manufacturer/manufacturer_form.html", {"form": form})


def manufacturer_update(request, pk):
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    if request.method == "POST":
        form = ManufacturerForm(request.POST, instance=manufacturer)
        if form.is_valid():
            form.save()
            return redirect("manufacturer_list")
    else:
        form = ManufacturerForm(instance=manufacturer)
    return render(request, "manufacturer/manufacturer_form.html", {"form": form})


def manufacturer_delete(request, pk):
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    if request.method == "POST":
        manufacturer.delete()
        return redirect("manufacturer_list")
    return render(
        request,
        "manufacturer/manufacturer_confirm_delete.html",
        {"manufacturer": manufacturer},
    )
