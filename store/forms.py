from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import User, Employee, Manufacturer, TypeOfProduct, Product, Client, Order


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["name", "age"]


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ["name", "location"]


class TypeOfProductForm(forms.ModelForm):
    class Meta:
        model = TypeOfProduct
        fields = ["name"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "type_of_product", "manufacturer", "price", "quantity"]


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "email", "phone_number", "age"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["employee", "client"]


class RegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=[("client", "Client"), ("employee", "Employee")],
        widget=forms.RadioSelect,
        required=True,
        initial="client",
    )
    phone_number = forms.CharField(required=True)
    age = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "phone_number", "age"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user_type = self.cleaned_data.get("user_type")
        name = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        phone_number = self.cleaned_data.get("phone_number")
        age = self.cleaned_data.get("age")

        if user_type == "client":
            user.is_client = True
            user.save()
            Client.objects.create(
                name=name, email=email, phone_number=phone_number, age=age
            )
        elif user_type == "employee":
            user.is_employee = True
            user.save()
            Employee.objects.create(
                name=name, email=email, phone_number=phone_number, age=age
            )

        return user
