# Dans reports/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Ou le nom de ta vue principale
]