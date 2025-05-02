from django.urls import path
from Football.views.views import webhook_receiver

urlpatterns = [
    path('webhook/', webhook_receiver, name='webhook_receiver'),
]
