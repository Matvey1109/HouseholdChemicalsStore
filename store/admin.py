from django.contrib import admin
from .models import (
    Slider,
    SliderSettings,
    User,
    Article,
    CompanyInfo,
    Term,
    Contact,
    Vacancy,
    Review,
    PromoCode,
    PickUpPoint,
    Employee,
    Product,
    TypeOfProduct,
    Manufacturer,
    Order,
    Client,
)

admin.site.register(User)
admin.site.register(Article)
admin.site.register(CompanyInfo)
admin.site.register(Term)
admin.site.register(Contact)
admin.site.register(Vacancy)
admin.site.register(Review)
admin.site.register(PromoCode)
admin.site.register(PickUpPoint)
admin.site.register(Employee)
admin.site.register(TypeOfProduct)
admin.site.register(Slider)
admin.site.register(SliderSettings)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "phone_number", "age"]


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "type_of_product", "price")
    list_filter = ("type_of_product",)
    search_fields = ("name",)


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("name", "location")
    list_per_page = 10
    list_filter = ("location",)


admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
