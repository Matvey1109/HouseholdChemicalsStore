from django.urls import path, re_path
from django.contrib.auth import views as login_views
from .views.pages_views import (
    array_task_view,
    checkbox_view,
    grapg_view,
    home_page_view,
    about_page_view,
    news_detail_page_view,
    news_page_view,
    scrolling_view,
    slider_settings_view,
    slider_view,
    terms_page_view,
    contacts_page_view,
    privacy_policy_page_view,
    vacancies_page_view,
    reviews_page_view,
    add_review_page_view,
    promocodes_page_view,
    pickuppoints_page_view,
    cart_page_view,
    payment_page_view,
)
from .views.employee_views import (
    employee_list,
    employee_detail,
    employee_create,
    employee_update,
    employee_delete,
)
from .views.manufacturer_views import (
    manufacturer_list,
    manufacturer_detail,
    manufacturer_create,
    manufacturer_update,
    manufacturer_delete,
)
from .views.type_of_product_views import (
    type_of_product_list,
    type_of_product_detail,
    type_of_product_create,
    type_of_product_update,
    type_of_product_delete,
)
from .views.product_views import (
    product_list,
    product_detail,
    product_create,
    product_update,
    product_delete,
)
from .views.client_views import (
    client_list,
    client_detail,
    client_create,
    client_update,
    client_delete,
)
from .views.order_views import (
    order_list,
    order_detail,
    order_create,
    order_update,
    order_delete,
)
from .views.auth_views import logout_view, register_view, profile_view
from .views.statistic_views import (
    demand_view,
    monthly_sales_volume_view,
    annual_sales_revenue_view,
    plot_statistics_view,
    sales_forecast_view,
)

pages_urls = [
    re_path(r"^$", home_page_view, name="home"),
    path("about/", about_page_view, name="about"),
    path("news/", news_page_view, name="news"),
    path("news_detail/<int:pk>/", news_detail_page_view, name="news_detail"),
    path("terms/", terms_page_view, name="terms"),
    path("contacts/", contacts_page_view, name="contacts"),
    path("privacy_policy/", privacy_policy_page_view, name="privacy_policy"),
    path("vacancies/", vacancies_page_view, name="vacancies"),
    path("reviews/", reviews_page_view, name="reviews"),
    # path("products/<int:pk>/add_review/", add_review_page_view, name="add_review"),
    re_path(
        r"^products/(?P<pk>\d+)/add_review/$", add_review_page_view, name="add_review"
    ),
    path("promocodes/", promocodes_page_view, name="promocodes"),
    path("pickuppoints/", pickuppoints_page_view, name="pickuppoints"),
    path("cart/", cart_page_view, name="cart"),
    path("payment/", payment_page_view, name="payment"),
    path("slider/", slider_view, name="slider"),
    path("slider/settings/", slider_settings_view, name="slider_settings"),
    path("checkbox/", checkbox_view, name="checkbox"),
    path("scrolling/", scrolling_view, name="scrolling"),
    path("array_task/", array_task_view, name="array_task"),
    path("graph/", grapg_view, name="graph"),
]

employee_urls = [
    path("employees/", employee_list, name="employee_list"),
    path("employees/<int:pk>/", employee_detail, name="employee_detail"),
    path("employees/create/", employee_create, name="employee_create"),
    path("employees/<int:pk>/update/", employee_update, name="employee_update"),
    path("employees/<int:pk>/delete/", employee_delete, name="employee_delete"),
]

manufacturer_urls = [
    path("manufacturers/", manufacturer_list, name="manufacturer_list"),
    path("manufacturers/<int:pk>/", manufacturer_detail, name="manufacturer_detail"),
    path("manufacturers/create/", manufacturer_create, name="manufacturer_create"),
    path(
        "manufacturers/<int:pk>/update/",
        manufacturer_update,
        name="manufacturer_update",
    ),
    path(
        "manufacturers/<int:pk>/delete/",
        manufacturer_delete,
        name="manufacturer_delete",
    ),
]

type_of_product_urls = [
    path("types/", type_of_product_list, name="type_of_product_list"),
    path("types/<int:pk>/", type_of_product_detail, name="type_of_product_detail"),
    path("types/create/", type_of_product_create, name="type_of_product_create"),
    path(
        "types/<int:pk>/update/", type_of_product_update, name="type_of_product_update"
    ),
    path(
        "types/<int:pk>/delete/", type_of_product_delete, name="type_of_product_delete"
    ),
]

product_urls = [
    path("products/", product_list, name="product_list"),
    path("products/<int:pk>/", product_detail, name="product_detail"),
    path("products/create/", product_create, name="product_create"),
    path("products/<int:pk>/update/", product_update, name="product_update"),
    path("products/<int:pk>/delete/", product_delete, name="product_delete"),
]

client_urls = [
    path("clients/", client_list, name="client_list"),
    path("clients/<int:pk>/", client_detail, name="client_detail"),
    path("clients/create/", client_create, name="client_create"),
    path("clients/<int:pk>/update/", client_update, name="client_update"),
    path("clients/<int:pk>/delete/", client_delete, name="client_delete"),
]

order_urls = [
    path("orders/", order_list, name="order_list"),
    path("orders/<int:pk>/", order_detail, name="order_detail"),
    path("orders/create/", order_create, name="order_create"),
    path("orders/<int:pk>/update/", order_update, name="order_update"),
    path("orders/<int:pk>/delete/", order_delete, name="order_delete"),
]

auth_urls = [
    path(
        "login/",
        login_views.LoginView.as_view(
            template_name="auth/login.html", next_page="profile"
        ),
        name="login",
    ),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("profile/", profile_view, name="profile"),
]

permission_urls = [
    path("superuser/demand", demand_view, name="demand"),
    path("superuser/monthly_sales", monthly_sales_volume_view, name="monthly_sales"),
    path("superuser/annual_sales", annual_sales_revenue_view, name="annual_sales"),
    path("superuser/plot_statistics", plot_statistics_view, name="plot_statistics"),
    path("superuser/sales_forecast", sales_forecast_view, name="sales_forecast"),
]

urlpatterns = []
urlpatterns += pages_urls
urlpatterns += employee_urls
urlpatterns += manufacturer_urls
urlpatterns += type_of_product_urls
urlpatterns += product_urls
urlpatterns += client_urls
urlpatterns += order_urls
urlpatterns += auth_urls
urlpatterns += permission_urls
