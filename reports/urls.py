# Dans reports/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='index'), # Ou le nom de ta vue principale
]