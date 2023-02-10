import requests
import os
import json
import uuid
from .models import Currency


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())  # Convert UUID format to a Python string.
    random = random.lower()  # Make all characters uppercase.
    random = random.replace("-", "")  # Remove the UUID '-'.
    # usage  = '%s-%s'%('TR',my_random_string(6))
    return random[0:string_length]  # Return the random string.


def get_default_currency():
    obj, created = Currency.objects.get_or_create(
        code="USD", defaults={"exchange_rate": 500}
    )
    return obj.pkid


def convert_currency_to_local(user_currency, product_currency, product_amount):
    """Converts the product price to the equivalent price in the users currency"""
    user_exchange_rate = Currency.objects.get(
        code=user_currency
    ).exchange_rate  # get user's exchange rate

    if product_currency != "USD":
        # if the product currency is not in USD, then
        # get the product exchange rate
        product_exchange_rate = Currency.objects.get(
            code=product_currency
        ).exchange_rate

        # divide the product amount by it's exchange rate to convert it to base form
        product_amount = product_amount / product_exchange_rate

    equivalent_amount = product_amount * user_exchange_rate
    return equivalent_amount


def get_conversion_rate(from_currency, to_currency, amount):

    url = f"https://api.apilayer.com/fixer/convert?to={to_currency}&from={from_currency}&amount={amount}"

    payload = {}
    headers = {"apikey": os.environ.get("CURRENCY_API")}

    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    if status_code == 200:
        result = response.text
        parsed_response = json.loads(result)

        return parsed_response["result"]
