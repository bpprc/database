from django.urls import path
from api import views

urlpatterns = [
    path('home_api', views.home_api, name='home_api'),
    path('needle_api_form', views.needle_api_form, name='needle_api_form'),
    path('needle_api_run', views.needle_api_run,
         name='needle_api_run'),
]
