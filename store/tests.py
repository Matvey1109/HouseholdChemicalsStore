from django.test import TestCase
from django.urls import reverse
from .models import (
    User,
    Article,
    CompanyInfo,
    Term,
    Contact,
    Employee,
    Vacancy,
    PromoCode,
    Client,
    Order,
    Product,
    TypeOfProduct,
    Manufacturer,
)
from .utils.date_utils import get_user_time, get_product_time
import calendar
from datetime import datetime


class PagesTests(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title="Test Article",
            content="Test Content",
            image="test.jpg",
        )
        self.company_info = CompanyInfo.objects.create(text="Company Information")
        self.term = Term.objects.create(
            question="Test Question",
            answer="Test Answer",
        )
        self.contact = Contact.objects.create(
            employee=Employee.objects.create(
                name="Test Employee",
                email="test@gmail.com",
                phone_number="+375 (29) 111-22-33",
                age=20,
            ),
            description="Test Description",
            photo="test.jpg",
        )
        self.vacancy = Vacancy.objects.create(
            title="Test Title",
            description="Test Description",
        )
        self.promocode = PromoCode.objects.create(
            code="TESTCODE",
            percentage=20,
            is_active=True,
        )

    def test_home_page_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)

    def test_about_page_view(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.company_info.text)

    def test_news_page_view(self):
        response = self.client.get(reverse("news"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)

    def test_terms_page_view(self):
        response = self.client.get(reverse("terms"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.term.question)

    def test_contacts_page_view(self):
        response = self.client.get(reverse("contacts"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contact.description)

    def test_privacy_policy_page_view(self):
        response = self.client.get(reverse("privacy_policy"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/privacy_policy_page.html")

    def test_vacancies_page_view(self):
        response = self.client.get(reverse("vacancies"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.vacancy.description)

    def test_promocodes_page_view(self):
        response = self.client.get(reverse("promocodes"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.promocode.code)


class AuthTests(TestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.profile_url = reverse("profile")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
            is_client=True,
            is_employee=False,
        )

    def test_register_view(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.register_url,
            {
                "username": "newuser",
                "password1": "newpassword",
                "password2": "newpassword",
                "email": "newuser@example.com",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.login_url, {"username": "newuser", "password": "newpassword"}
        )
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        self.client.login(username="newuser", password="newpassword")
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("product_list"))

    def test_user_model(self):
        self.assertEqual(self.user.is_client, True)
        self.assertEqual(self.user.is_employee, False)


class ClientTests(TestCase):
    def setUp(self):
        self.client_data = {
            "name": "Test Client",
            "email": "testclient@example.com",
            "phone_number": "+375 (29) 111-22-33",
            "age": 20,
        }
        self.client_instance = Client.objects.create(**self.client_data)

    def test_client_list_view(self):
        response = self.client.get(reverse("client_list"))
        self.assertEqual(response.status_code, 200)

    def test_client_detail_view(self):
        response = self.client.get(
            reverse("client_detail", args=[self.client_instance.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_client_create_view(self):
        response = self.client.get(reverse("client_create"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse("client_create"), data=self.client_data)
        self.assertEqual(response.status_code, 302)

    def test_client_update_view(self):
        response = self.client.get(
            reverse("client_update", args=[self.client_instance.pk])
        )
        self.assertEqual(response.status_code, 200)

        updated_data = {
            "name": "Updated Client",
            "email": "testclient@example.com",
            "phone_number": "+375 (29) 111-22-33",
            "age": 30,
        }
        response = self.client.post(
            reverse("client_update", args=[self.client_instance.pk]), data=updated_data
        )
        self.assertEqual(response.status_code, 302)
        self.client_instance.refresh_from_db()

    def test_client_delete_view(self):
        response = self.client.get(
            reverse("client_delete", args=[self.client_instance.pk])
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("client_delete", args=[self.client_instance.pk])
        )
        self.assertEqual(response.status_code, 302)

        self.assertFalse(Client.objects.filter(pk=self.client_instance.pk).exists())


class EmployeeTests(TestCase):
    def setUp(self):
        self.employee_data = {
            "name": "Test Employee",
            "email": "testemployee@example.com",
            "phone_number": "+375 (29) 111-22-33",
            "age": 20,
        }
        self.employee_instance = Employee.objects.create(**self.employee_data)

    def test_employee_list_view(self):
        response = self.client.get(reverse("employee_list"))
        self.assertEqual(response.status_code, 200)

    def test_employee_detail_view(self):
        response = self.client.get(
            reverse("employee_detail", args=[self.employee_instance.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_employee_create_view(self):
        response = self.client.get(reverse("employee_create"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse("employee_create"), data=self.employee_data)
        self.assertEqual(response.status_code, 302)

    def test_employee_update_view(self):
        response = self.client.get(
            reverse("employee_update", args=[self.employee_instance.pk])
        )
        self.assertEqual(response.status_code, 200)

        updated_data = {
            "name": "Updated Employee",
            "email": "testemployee@example.com",
            "phone_number": "+375 (29) 111-22-33",
            "age": 30,
        }
        response = self.client.post(
            reverse("employee_update", args=[self.employee_instance.pk]),
            data=updated_data,
        )
        self.assertEqual(response.status_code, 302)
        self.employee_instance.refresh_from_db()

    def test_employee_delete_view(self):
        response = self.client.get(
            reverse("employee_delete", args=[self.employee_instance.pk])
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("employee_delete", args=[self.employee_instance.pk])
        )
        self.assertEqual(response.status_code, 302)

        self.assertFalse(Employee.objects.filter(pk=self.employee_instance.pk).exists())


class TypeOfProductTests(TestCase):
    def setUp(self):
        self.type_of_product_data = {
            "name": "Test Type",
        }
        self.type_of_product_instance = TypeOfProduct.objects.create(
            **self.type_of_product_data
        )

    def test_type_of_product_list_view(self):
        response = self.client.get(reverse("type_of_product_list"))
        self.assertEqual(response.status_code, 200)

    def test_type_of_product_detail_view(self):
        response = self.client.get(
            reverse("type_of_product_detail", args=[self.type_of_product_instance.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_type_of_product_create_view(self):
        response = self.client.get(reverse("type_of_product_create"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("type_of_product_create"), data=self.type_of_product_data
        )
        self.assertEqual(response.status_code, 302)

    def test_type_of_product_update_view(self):
        response = self.client.get(
            reverse("type_of_product_update", args=[self.type_of_product_instance.pk])
        )
        self.assertEqual(response.status_code, 200)

        updated_data = {
            "name": "Updated Type",
        }
        response = self.client.post(
            reverse("type_of_product_update", args=[self.type_of_product_instance.pk]),
            data=updated_data,
        )
        self.assertEqual(response.status_code, 302)
        self.type_of_product_instance.refresh_from_db()

    def test_type_of_product_delete_view(self):
        response = self.client.get(
            reverse("type_of_product_delete", args=[self.type_of_product_instance.pk])
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("type_of_product_delete", args=[self.type_of_product_instance.pk])
        )
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            TypeOfProduct.objects.filter(pk=self.type_of_product_instance.pk).exists()
        )


class ManufacturerTests(TestCase):
    def setUp(self):
        self.manufacturer_data = {
            "name": "Test Manufacturer",
            "location": "Test Location",
        }
        self.manufacturer_instance = Manufacturer.objects.create(
            **self.manufacturer_data
        )

    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("manufacturer_list"))
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_detail_view(self):
        response = self.client.get(
            reverse("manufacturer_detail", args=[self.manufacturer_instance.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_create_view(self):
        response = self.client.get(reverse("manufacturer_create"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("manufacturer_create"), data=self.manufacturer_data
        )
        self.assertEqual(response.status_code, 302)

    def test_manufacturer_update_view(self):
        response = self.client.get(
            reverse("manufacturer_update", args=[self.manufacturer_instance.pk])
        )
        self.assertEqual(response.status_code, 200)

        updated_data = {
            "name": "Updated Type",
            "location": "Updated Location",
        }
        response = self.client.post(
            reverse("manufacturer_update", args=[self.manufacturer_instance.pk]),
            data=updated_data,
        )
        self.assertEqual(response.status_code, 302)
        self.manufacturer_instance.refresh_from_db()

    def test_manufacturer_delete_view(self):
        response = self.client.get(
            reverse("manufacturer_delete", args=[self.manufacturer_instance.pk])
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("manufacturer_delete", args=[self.manufacturer_instance.pk])
        )
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Manufacturer.objects.filter(pk=self.manufacturer_instance.pk).exists()
        )


class UtilsTests(TestCase):
    def test_get_user_time(self):
        result = get_user_time()

        self.assertIsInstance(result, dict)
        self.assertIn("user_timezone", result)
        self.assertIn("current_date_formatted", result)
        self.assertIn("calendar_text", result)

        self.assertIsNotNone(result["user_timezone"])

        self.assertIsInstance(result["current_date_formatted"], str)
        self.assertRegex(result["current_date_formatted"], r"\d{2}/\d{2}/\d{4}")

        self.assertIsInstance(result["calendar_text"], str)
        self.assertIn(
            calendar.month_name[datetime.now().month], result["calendar_text"]
        )

    def test_get_product_time(self):
        product = Product.objects.create(
            name="Sample Product",
            type_of_product=TypeOfProduct.objects.create(name="Sample Type"),
            manufacturer=Manufacturer.objects.create(
                name="Sample Manufacturer", location="Sample Location"
            ),
            price=10.99,
            quantity=5,
        )

        created_tz, updated_tz, created_utc, updated_utc = get_product_time(product)

        self.assertIsInstance(created_tz, str)
        self.assertRegex(created_tz, r"\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2}")
        self.assertIsInstance(updated_tz, str)
        self.assertRegex(updated_tz, r"\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2}")
        self.assertIsInstance(created_utc, str)
        self.assertRegex(created_utc, r"\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2}")
        self.assertIsInstance(updated_utc, str)
        self.assertRegex(updated_utc, r"\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2}")

        product.delete()


class ProductTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="ACME Corporation",
            location="New York",
        )
        self.type_of_product = TypeOfProduct.objects.create(
            name="Electronics",
        )
        self.product_data = {
            "name": "Laptop",
            "type_of_product": self.type_of_product,
            "manufacturer": self.manufacturer,
            "price": 1000,
            "quantity": 10,
        }
        self.product_instance = Product.objects.create(**self.product_data)

    def test_product_list_view(self):
        response = self.client.get(reverse("product_list"))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view(self):
        response = self.client.get(
            reverse("product_detail", args=[self.product_instance.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_product_create_view(self):
        response = self.client.get(reverse("product_create"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("product_create"), data=self.product_data
        )
        self.assertEqual(response.status_code, 200)

    def test_product_update_view(self):
        response = self.client.get(
            reverse("product_update", args=[self.product_instance.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_product_delete_view(self):
        response = self.client.get(
            reverse("product_delete", args=[self.product_instance.pk])
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("product_delete", args=[self.product_instance.pk])
        )
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Product.objects.filter(pk=self.product_instance.pk).exists()
        )


class OrderTestCase(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            name="John Doe",
            email="john@example.com",
            phone_number="+375 (29) 123-45-67",
            age=25,
        )
        self.manufacturer = Manufacturer.objects.create(
            name="ACME Corporation", location="New York"
        )
        self.type_of_product = TypeOfProduct.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Laptop",
            type_of_product=self.type_of_product,
            manufacturer=self.manufacturer,
            price=1000,
            quantity=10,
        )
        self.order = Order.objects.create(
            employee=self.employee,
            client=Client.objects.create(
                name="Jane Smith",
                email="jane@example.com",
                phone_number="+375 (29) 987-65-43",
                age=30,
            ),
            total_price=2000.0,
            product_quantities={},
        )
        self.order.products.add(self.product)
        self.order.save()

    def test_order_list_view(self):
        response = self.client.get(reverse("order_list"))
        self.assertEqual(response.status_code, 302)

        redirect_url = response.url
        response = self.client.get(redirect_url)
        self.assertEqual(response.status_code, 200)

    def test_order_detail_view(self):
        response = self.client.get(reverse("order_detail", args=[self.order.pk]))
        self.assertEqual(response.status_code, 302)

        redirect_url = response.url
        response = self.client.get(redirect_url)
        self.assertEqual(response.status_code, 200)

    def test_order_create_view(self):
        form_data = {
            "employee": self.employee.pk,
            "client": Client.objects.create(
                name="Jane Smith",
                email="jane@example.com",
                phone_number="+375 (29) 987-65-43",
                age=30,
            ).pk,
            "products": [self.product.pk],
            "quantity_{}".format(self.product.pk): 1,
        }
        response = self.client.post(reverse("order_create"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
