from celery.schedules import crontab
from celery import Celery
from .models import Currency
from .utils import get_conversion_rate


app = Celery()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(
            hour="0, 8, 16",
            minute=0,
        ),
        update_exchange_rates.s(),
    )


@app.task
def update_exchange_rates():
    try:
        currencies = Currency.objects.all()

        for currency in currencies:
            conversion_rate = get_conversion_rate(currency.code, "USD", 1)
            currency.exchange_rate = conversion_rate
            currency.save()
    except Exception as e:
        # TODO use a logger to log the error
        print(e)
