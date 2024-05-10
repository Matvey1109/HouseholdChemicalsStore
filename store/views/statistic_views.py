# from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Sum
from django.shortcuts import render
from django.utils.timezone import now
import calendar
import matplotlib
from datetime import datetime, timedelta

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from statistics import mean, mode, median
from ..models import Product, TypeOfProduct, Order, Client
from ..decorators import superuser_required


@superuser_required
def demand_view(
    request,
):  # Товар, пользующийся наибольшим спросом; Товар, не пользующийся спросом;
    product_in_greatest_demand = (
        Product.objects.annotate(order_count=Count("order"))
        .order_by("-order_count")
        .first()
    )

    product_not_in_demand = (
        Product.objects.annotate(order_count=Count("order"))
        .filter(order_count=0)
        .last()
    )

    return render(
        request,
        "statistic/demand.html",
        {
            "product_in_greatest_demand": product_in_greatest_demand,
            "product_not_in_demand": product_not_in_demand,
        },
    )


@superuser_required
def monthly_sales_volume_view(
    request,
):  # Ежемесячный объем продаж товаров каждого вида; объемам и поступлениям от продаж;
    current_month_number = now().month
    current_year = now().year

    sales_volume = (
        Order.objects.filter(
            date_ordered__year=current_year, date_ordered__month=current_month_number
        )
        .values("products__type_of_product")
        .annotate(sales_volume=Sum("product_quantities__quantity"))
        .annotate(product_count=Count("products__type_of_product"))
    )

    result = {}
    for item in sales_volume:
        product_type = TypeOfProduct.objects.get(pk=item["products__type_of_product"])
        result[product_type.name] = {
            "current_month": calendar.month_name[current_month_number],
            "product_count": item["product_count"],
        }

    df = pd.DataFrame.from_dict(result, orient="index")
    pivot_table = df.pivot_table(
        values="product_count", index="current_month", columns=df.index
    )

    return render(
        request, "statistic/monthly_sales_volume.html", {"pivot_table": pivot_table}
    )


@superuser_required
def annual_sales_revenue_view(request):  # Годовой отчет поступлений от продаж;
    current_year = now().year

    sales_revenue = (
        Order.objects.filter(date_ordered__year=current_year)
        .values("date_ordered__month")
        .annotate(total_revenue=Sum("total_price"))
    )

    result = {}
    for item in sales_revenue:
        month_number = item["date_ordered__month"]
        total_revenue = item["total_revenue"]
        result[calendar.month_name[month_number]] = total_revenue

    return JsonResponse(result)


@superuser_required
def plot_statistics_view(request):
    num_customers = Client.objects.count()

    product_counts = TypeOfProduct.objects.annotate(order_count=Count("product"))

    # Объем продаж
    sales_revenues = TypeOfProduct.objects.annotate(total_revenue=Sum("product__price"))

    # Поступления от продаж
    sales_volumes = TypeOfProduct.objects.annotate(
        total_volume=Sum("product__quantity")
    )

    product_labels = [product.name for product in product_counts]
    order_counts = [product.order_count for product in product_counts]
    revenue_values = [product.total_revenue for product in sales_revenues]
    volume_values = [product.total_volume for product in sales_volumes]

    plt.figure(figsize=(10, 6))

    plt.subplot(2, 2, 1)
    plt.bar(["Customers"], [num_customers])
    plt.title("Number of Customers")
    plt.ylabel("Count")

    plt.subplot(2, 2, 2)
    plt.bar(product_labels, order_counts)
    plt.title("Product Counts")
    plt.xlabel("Type of Product")
    plt.ylabel("Count")

    plt.subplot(2, 2, 3)
    plt.bar(product_labels, revenue_values)
    plt.title("Sales Revenues")
    plt.xlabel("Type of Product")
    plt.ylabel("Revenue")

    plt.subplot(2, 2, 4)
    plt.bar(product_labels, volume_values)
    plt.title("Sales Volumes")
    plt.xlabel("Type of Product")
    plt.ylabel("Volume")

    response = HttpResponse(content_type="image/png")
    plt.savefig(response, format="png")
    plt.close()

    return response


@superuser_required
def sales_forecast_view(
    request,
):  # Линейный тренд продаж, Прогноз продаж, статистические показатели (среднее, мода и медиана) по сумме продаж
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)

    sales_amounts = Order.objects.filter(
        date_ordered__range=[start_date, end_date]
    ).values_list("total_price", flat=True)

    total_sales = sum(sales_amounts)
    total_sales = total_sales or 0

    days = (end_date - start_date).days + 1
    average_daily_sales = total_sales / days

    projected_sales = average_daily_sales * 30

    sales_mean = mean(sales_amounts)
    sales_mode = mode(sales_amounts)
    sales_median = median(sales_amounts)

    context = {
        "start_date": start_date,
        "end_date": end_date,
        "total_sales": total_sales,
        "average_daily_sales": average_daily_sales,
        "projected_sales": projected_sales,
        "sales_mean": sales_mean,
        "sales_mode": sales_mode,
        "sales_median": sales_median,
    }

    return render(request, "statistic/sales_forecast.html", context)
