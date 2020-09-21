from django.urls import path
from namingalgorithm import views

urlpatterns = [
    #path('', views.send_mail, name='sendmail'),
    path('admin/contact/', views.contactView, name='contact'),
    path('admin/success/', views.successView, name='success'),
    path('submit_home/', views.submit_home, name='submit_home'),
    path('submit/', views.submit, name='submit'),
    path('naming_algorithm/', views.naming_algorithm, name='naming_algorithm'),
    path('run_naming_algorithm/', views.run_naming_algorithm,
         name='run_naming_algorithm'),
    path('run_align/', views.run_align, name='run_align'),
    path('align_results/', views.align_results, name='align_results')
]
