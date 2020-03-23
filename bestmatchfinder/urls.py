from django.contrib import admin
from django.urls import path, include
from bestmatchfinder import views

urlpatterns = [
    path('bestmatchfinder_home/', views.bestmatchfinder_home,
         name='bestmatchfinder_home'),
    path('bestmatchfinder_database/', views.bestmatchfinder_database,
         name='bestmatchfinder_database'),
    path('run_needle_server/', views.run_needle_server, name='run_needle_server'),
    path('run_needle_server_celery/', views.run_needle_server_celery,
         name='run_needle_server_celery'),
    path('taskstatus_needle_celery/<str:task_id>/', views.taskstatus_needle_celery,
         name='taskstatus_needle_celery'),
    path('celery_task_status/<str:task_id>/', views.celery_task_status,
         name='celery_task_status'),
    path('bestmatchfinder_database_sequence_run/', views.bestmatchfinder_database_sequence_run,
         name='bestmatchfinder_database_sequence_run'),
]
