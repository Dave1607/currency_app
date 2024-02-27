from .models import Currency,Subscribers
from django.http import JsonResponse,HttpResponse,HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    try:        
        # Extract exchange rates
        exchange_rates = Currency.get_exchange_rates()
        
        # Prepare the response content
        content = {
            'rates': exchange_rates,
        }
        
        # Return JSON response
        return JsonResponse(content,status = 200)

    except ObjectDoesNotExist:
        # Handle the case where Currency object does not exist
        return JsonResponse({'error': 'Currency data not available'}, status=500)
    
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': str(e)}, status=500)
    
def convert(request):
    #convert one currency to another
    try:
        rate = Currency.converter(
            request.POST.get('from_'),
            request.POST.get('to_'),
            request.POST.get('amount')
            )
        if rate:
            return JsonResponse({'status': 200,'rate': rate}, safe=False)
        else:
            return JsonResponse({'error': 'No data'}, safe=False)
    except Exception as e:
        return JsonResponse({'error': 'Internal Server Error'}, status=500)

def rate_reminder_register(request):
    try:
        # add email to reminders list and save it in the database
        name = request.POST.get('name')
        email = request.POST.get('email')
        currency_code = request.POST.get('currency_code')

        try:
            Currency.objects.get(currency_code=currency_code)
            Subscribers.objects.create(
                name=name,
                email=email,
                currency_code=currency_code
            )
            return JsonResponse({"message": "Email registered successfully!"})
        except Currency.DoesNotExist:
            return HttpResponse("Invalid currency code")
    except KeyError:
        return HttpResponseBadRequest("Missing parameter")

def rate_reminder_cancelation(request):
    # remove email from reminders list
    if Subscribers.DoesNotExist(email = request.POST.get('email')):
        return JsonResponse({"error":"This email is not registered"})
    else:
        subscriber = Subscribers.objects.get(email = request.POST.get('email'))
        subscriber.delete()
        return JsonResponse({"message":"Removed Successfully!"})