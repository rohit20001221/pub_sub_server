from django.urls import path
from . import views

urlpatterns = [
    path('mqtt/get/<topic>', views.MqttRestGetAPI.as_view()),
    path('mqtt/post/<topic>', views.MqttRestPostAPI.as_view()),
]