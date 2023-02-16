from .models import Currency
from .utils import get_conversion_rate
from celery import shared_task


# Define the task to update exchange rates for a single currency
@shared_task()
def update_exchange_rates():
    """
    This Celery task updates the exchange rate for each currency in the database using the get_conversion_rate utility function.
    """
    try:
        currencies = Currency.objects.all()

        for currency in currencies:
            # Call the get_conversion_rate function to update the exchange rate for this currency
            conversion_rate = get_conversion_rate("USD", currency.code, 1)
            currency.exchange_rate = conversion_rate
            currency.save()
            print(f"{currency.code} was updated successfully")
    except Exception as e:
        print(e)
        # Log the error using the Celery logger
        print("Failed to update exchange rates: %s", e)
