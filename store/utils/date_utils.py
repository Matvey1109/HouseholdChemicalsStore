from datetime import datetime
import calendar
import tzlocal
from ..models import Product


def get_user_time():
    user_timezone = tzlocal.get_localzone()
    current_date = datetime.now(user_timezone).date()
    current_date_formatted = current_date.strftime("%d/%m/%Y")

    calendar_text = calendar.month(
        datetime.now(user_timezone).year,
        datetime.now(user_timezone).month,
    )

    return {
        "user_timezone": user_timezone,
        "current_date_formatted": current_date_formatted,
        "calendar_text": calendar_text,
    }


def get_product_time(product: Product):
    user_timezone = tzlocal.get_localzone()
    created_tz = product.created_at.astimezone(user_timezone).strftime(
        "%d/%m/%Y - %H:%M:%S"
    )
    updated_tz = product.updated_at.astimezone(user_timezone).strftime(
        "%d/%m/%Y - %H:%M:%S"
    )
    created_utc = product.created_at.strftime("%d/%m/%Y - %H:%M:%S")
    updated_utc = product.updated_at.strftime("%d/%m/%Y - %H:%M:%S")
    return created_tz, updated_tz, created_utc, updated_utc
