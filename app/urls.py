from django.urls import path
from .views import index,convert,rate_reminder_register,rate_reminder_cancelation

urlpatterns = [
    path('', index, name= 'index'),
    path('convert/',convert, name='convert'),
    path('rate-reminder/',rate_reminder_register,name='rate_reminder_register'),
    path('rate-reminder/cancel',rate_reminder_cancelation,name='rate_reminder_cancel')
]