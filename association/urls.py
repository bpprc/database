from django.urls import path
from association import views

urlpatterns = [
    path('', views.send_mail, name='sendmail'),
]
