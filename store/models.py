from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CompanyInfo(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class Term(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.question


class Contact(models.Model):
    employee = models.OneToOneField("Employee", on_delete=models.CASCADE)
    description = models.TextField()
    photo = models.ImageField()

    def __str__(self):
        return self.employee.name


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(
        choices=(
            (1, "1 Star"),
            (2, "2 Stars"),
            (3, "3 Stars"),
            (4, "4 Stars"),
            (5, "5 Stars"),
        )
    )
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(99)],
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class PickUpPoint(models.Model):
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.address


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r"^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$",
        message="Phone number must be in the format '+375 (29) XXX-XX-XX'",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=20, null=True)
    age = models.PositiveIntegerField(validators=[MinValueValidator(18)])

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TypeOfProduct(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    type_of_product = models.ForeignKey(TypeOfProduct, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r"^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$",
        message="Phone number must be in the format '+375 (29) XXX-XX-XX'",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=20, null=True)
    age = models.PositiveIntegerField(validators=[MinValueValidator(18)])

    def __str__(self):
        return self.name


class Order(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_ordered = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    product_quantities = models.JSONField(encoder=DjangoJSONEncoder, default=dict)

    def __str__(self):
        return f"Order #{self.pk} - {self.client.name} - {self.date_ordered}"
