from django.shortcuts import render, get_object_or_404, redirect
from ..models import Client
from ..forms import ClientForm
from ..utils.api_utils import get_client_gender, get_client_nationality


def client_list(request):
    clients = Client.objects.all()
    return render(
        request,
        "client/client_list.html",
        {"clients": clients},
    )


def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client_gender = get_client_gender(client_name=client.name)
    client_nationality = get_client_nationality(client_name=client.name)
    return render(
        request,
        "client/client_detail.html",
        {
            "client": client,
            "client_gender": client_gender,
            "client_nationality": client_nationality,
        },
    )


def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("client_list")
    else:
        form = ClientForm()
    return render(request, "client/client_form.html", {"form": form})


def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect("client_list")
    else:
        form = ClientForm(instance=client)
    return render(request, "client/client_form.html", {"form": form})


def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        client.delete()
        return redirect("client_list")
    return render(
        request,
        "client/client_confirm_delete.html",
        {"client": client},
    )
