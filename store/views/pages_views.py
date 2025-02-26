from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from ..models import (
    Article,
    CompanyInfo,
    Slider,
    SliderSettings,
    Term,
    Contact,
    Vacancy,
    Review,
    PromoCode,
    PickUpPoint,
    Product,
)
from ..forms import SliderSettingsForm
import logging
from ..decorators import client_required

logger = logging.getLogger(__name__)


def home_page_view(request):
    try:
        latest_article = Article.objects.latest("published_date")
    except Article.DoesNotExist:
        latest_article = None
    context = {"latest_article": latest_article}
    logger.log(settings.LOGGING_LEVELS["info"], "VIEW: home_page_view")
    return render(request, "pages/home_page.html", context)


def about_page_view(request):
    company_info = CompanyInfo.objects.first()
    context = {"company_info": company_info}
    logger.log(settings.LOGGING_LEVELS["info"], "VIEW: about_page_view")
    return render(request, "pages/about_page.html", context)


def news_page_view(request):
    news = Article.objects.all()
    context = {"news": news}
    logger.log(settings.LOGGING_LEVELS["info"], "VIEW: news_page_view")
    return render(request, "pages/news_page.html", context)


def news_detail_page_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, "pages/news_detail_page.html", {"article": article})


def terms_page_view(request):
    terms = Term.objects.all()
    context = {"terms": terms}
    logger.log(settings.LOGGING_LEVELS["info"], "VIEW: terms_page_view")
    return render(request, "pages/terms_page.html", context)


def contacts_page_view(request):
    contacts = Contact.objects.all()
    context = {"contacts": contacts}
    logger.log(settings.LOGGING_LEVELS["info"], "VIEW: contacts_page_view")
    return render(request, "pages/contacts_page.html", context)


def privacy_policy_page_view(request):
    logger.log(settings.LOGGING_LEVELS["info"], "VIEW: privacy_policy_page_view")
    return render(request, "pages/privacy_policy_page.html")


def vacancies_page_view(request):
    vacancies = Vacancy.objects.all()
    context = {"vacancies": vacancies}
    logger.log(settings.LOGGING_LEVELS["info"], "VIEW: vacancies_page_view")
    return render(request, "pages/vacancies_page.html", context)


def reviews_page_view(request):
    reviews = Review.objects.all().order_by("-date_added")
    context = {"reviews": reviews}
    logger.log(settings.LOGGING_LEVELS["info"], "VIEW: reviews_page_view")
    return render(request, "pages/reviews_page.html", context)


@login_required
def add_review_page_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    logger.log(settings.LOGGING_LEVELS["warning"], "VIEW: add_review_page_view")

    if request.method == "POST":
        rating = request.POST.get("rating")
        text = request.POST.get("text")

        review = Review.objects.create(
            user=request.user, product=product, rating=rating, text=text
        )
        review.save()
        return redirect("product_detail", pk=product.id)

    return render(request, "pages/add_review_page.html", context)


def promocodes_page_view(request):
    promocodes = PromoCode.objects.all()
    context = {"promocodes": promocodes}
    logger.log(settings.LOGGING_LEVELS["info"], "VIEW: promocodes_page_view")
    return render(request, "pages/promocodes_page.html", context)


@client_required
def pickuppoints_page_view(request):
    pickuppoints = PickUpPoint.objects.all()
    context = {"pickuppoints": pickuppoints}
    logger.log(settings.LOGGING_LEVELS["info"], "VIEW: pickuppoint_page_view")
    return render(request, "pages/pickuppoint_page.html", context)


def cart_page_view(request):
    logger.log(settings.LOGGING_LEVELS["info"], "VIEW: cart_page_view")
    return render(request, "pages/cart_page.html")


def payment_page_view(request):
    logger.log(settings.LOGGING_LEVELS["info"], "VIEW: payment_page_view")
    return render(request, "pages/payment_page.html")


def slider_view(request):
    slides = Slider.objects.all()
    settings = SliderSettings.objects.first()
    return render(
        request, "pages/slider.html", {"slides": slides, "settings": settings}
    )


def slider_settings_view(request):
    settings = SliderSettings.objects.first()
    if request.method == "POST":
        form = SliderSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect("slider")
    else:
        form = SliderSettingsForm(instance=settings)
    return render(request, "pages/slider_settings.html", {"form": form})


def checkbox_view(request):
    return render(request, "pages/checkbox.html")


def scrolling_view(request):
    return render(request, "pages/scrolling.html")


def array_task_view(request):
    return render(request, "pages/array_task.html")


def grapg_view(request):
    return render(request, "pages/graph.html")
