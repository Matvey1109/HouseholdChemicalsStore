from django.shortcuts import render, get_object_or_404, redirect
from ..models import Employee
from ..forms import EmployeeForm


def employee_list(request):
    employees = Employee.objects.all()
    return render(request, "employee/employee_list.html", {"employees": employees})


def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, "employee/employee_detail.html", {"employee": employee})


def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("employee_list")
    else:
        form = EmployeeForm()
    return render(request, "employee/employee_form.html", {"form": form})


def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect("employee_list")
    else:
        form = EmployeeForm(instance=employee)
    return render(request, "employee/employee_form.html", {"form": form})


def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        employee.delete()
        return redirect("employee_list")
    return render(
        request, "employee/employee_confirm_delete.html", {"employee": employee}
    )
