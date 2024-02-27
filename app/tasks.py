from __future__ import  absolute_import,unicode_literals
from celery import shared_task
from .models import Currency,Subscribers

@shared_task
def daily_task():
    # Update current currency rates
    currency = Currency()
    currency.update_current_rate()

    # Send notifications to subscribed users about changes in the exchange rate of currencies
    subscribers = Subscribers()
    subscribers.send_rate_updates()