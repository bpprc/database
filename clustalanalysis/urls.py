from django.urls import path
from clustalanalysis import views

urlpatterns = [
    # path('draw_phylo/', views.draw_phylo ,name='draw_phylo'),
    path('domain_analysis_homepage/', views.domain_analysis_homepage,
         name='domain_analysis_homepage'),
    path('domain_analysis/', views.domain_analysis, name='domain_analysis'),
    path('dendogram/', views.dendogram, name='dendogram'),
    path('dendogram_homepage/', views.dendogram_homepage,
         name='dendogram_homepage'),
    path('domain_analysis_homepage/', views.domain_analysis_homepage,
         name='domain_analysis_homepage'),
    path('domain_analysis/', views.domain_analysis, name='domain_analysis'),
    path('dendogram/', views.dendogram, name='dendogram'),
    path('dendogram_homepage/', views.dendogram_homepage,
         name='dendogram_homepage'),
    path('dendogram_homepage2/', views.dendogram_homepage2,
         name='dendogram_homepage2'),
    path('dendogram_celery/', views.dendogram_celery,
         name='dendogram_celery'),
    path('taskstatus_clustal_celery/<str:task_id>/', views.taskstatus_clustal_celery,
         name='taskstatus_clustal_celery'),
    path('celery_task_status_clustal/<str:task_id>/', views.celery_task_status_clustal,
         name='celery_task_status_clustal'),
    path('protein_analysis/', views.protein_analysis, name='protein_analysis'),
    # path('domain_phylo/', views.domain_phylo ,name='domain_phylo'),
]
