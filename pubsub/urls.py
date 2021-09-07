from django.urls import path
from . import views

urlpatterns = [
    path('mqtt/<topic>', views.MqttRestAPI.as_view()),
]