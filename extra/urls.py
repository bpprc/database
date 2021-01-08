from django.contrib import admin
from django.urls import path, include
from extra import views

urlpatterns = [
    path('feedback_home/', views.feedback_home,
         name='feedback_home'),
    path('github_home/', views.github_home,
         name='github_home'),
    path('faq/', views.faq,
         name='faq'),
]
