from prediction.views import predict
from django.urls import path

urlpatterns = [
    path('', predict, name='predict'),
]
