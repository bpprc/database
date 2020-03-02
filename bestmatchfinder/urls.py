from django.contrib import admin
from django.urls import path, include
from bestmatchfinder import views

urlpatterns = [
    path('bestmatchfinder_home/', views.bestmatchfinder_home ,name='bestmatchfinder_home'),
    path('bestmatchfinder_database/', views.bestmatchfinder_database ,name='bestmatchfinder_database'),
    path('run_needle_server/', views.run_needle_server ,name='run_needle_server'),
    path('bestmatchfinder_database_sequence_run/', views.bestmatchfinder_database_sequence_run ,name='bestmatchfinder_database_sequence_run'),
]
