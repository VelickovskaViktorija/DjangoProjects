# FILE: views.py
# Почетна страна: прикажување на недвижности > 100 m2 и не се продадени
from django.shortcuts import render
from .models import Property

def home(request):
    properties = Property.objects.filter(is_sold=False, area__gt=100)
    return render(request, 'home.html', {'properties': properties})


# FILE: urls.py
# URL рутирање за почетната страна
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]