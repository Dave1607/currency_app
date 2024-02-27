from django.db import models
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import uuid
import datetime
import requests

class Currency(models.Model):
    id = models.UUIDField(primary_key=True,unique=True)
    currency_code = models.CharField(max_length=3)
    rate_to_dollar = models.FloatField()
    updated_at = models.DateField()

    def __str__(self):
        return self.currency_code
    
    def update_current_rate(self):
        url = 'https://api.exchangerate-api.com/v4/latest/USD'
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            for currency_code, rate in data['rates'].items():
                try:
                    currency = Currency.objects.get(currency_code=currency_code)
                    currency.rate_to_dollar = rate
                    currency.updated_at = datetime.datetime.strptime(data['date'], "%Y-%m-%d").date()
                    currency.save()
                except ObjectDoesNotExist:
                    new_currency = Currency.objects.create(
                        id=uuid.uuid4(),
                        currency_code=currency_code,
                        rate_to_dollar=rate,
                        updated_at=datetime.datetime.strptime(data['date'], "%Y-%m-%d").date()
                    )
                    new_currency.save()
            return True
        else:
            raise Exception('API is not available')
            
        
    def converter(from_,to_,amount):
        try:
            from_cur = Currency.objects.get(currency_code=from_)
            to_cur = Currency.objects.get(currency_code=to_)
            
            result = amount * (to_cur.rate_to_dollar / from_cur.rate_to_dollar)
            return round(result, 2)
        except Currency.DoesNotExist:
            return "Currency does not exist"
            
    def get_exchange_rates():
        base_currency = 'USD'
        rates = {}
        for currency_obj in Currency.objects.all():
            rates[currency_obj.currency_code] = round(currency_obj.rate_to_dollar,2)

        sorted_rates = dict(sorted(rates.items()))
        rates[base_currency] =  1
        return {
            "base": base_currency,
            "date": str(datetime.date.today()),
            "rates": sorted_rates
        }
    
class Subscribers(models.Model):
    name = models.CharField(max_length = 50)
    email = models.EmailField(unique=True)
    currency_code = models.CharField(max_length = 3)
    
    def __str__(self) -> str:
        return self.email

    def send_rate_updates(self):
        current_rate = Currency.get_exchange_rates()
        for  subscriber in Subscribers.objects.all():
            user = Subscribers.objects.get(email = subscriber.email)
            email_subject = f'Rate Update {current_rate['date']}- Exchange Rate App'
            email_content = {
                'name':user.name,
                'currency':subscriber.currency_code,
                'rate' : Currency.objects.get(currency_code = user.currency_code).rate_to_dollar,
                'date': current_rate['date'],
                'base': current_rate['base'],
            }
            email_body =  render_to_string("rate_updates.html", {'content':email_content})
            msg = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [subscriber.email],
                reply_to=None
                )
            msg.content_subtype = "html"
            msg.send()