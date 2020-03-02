from django.contrib import admin
from django.urls import path, include
from clustalanalysis import views

urlpatterns = [
    # path('draw_phylo/', views.draw_phylo ,name='draw_phylo'),
    path('domain_analysis_homepage/', views.domain_analysis_homepage ,name='domain_analysis_homepage'),
    path('domain_anlaysis/', views.domain_anlaysis ,name='domain_anlaysis'),
    path('dendogram/', views.dendogram ,name='dendogram'),
    path('dendogram_homepage/', views.dendogram_homepage ,name='dendogram_homepage'),
    path('protein_analysis/', views.protein_analysis, name='protein_analysis'),
    # path('domain_phylo/', views.domain_phylo ,name='domain_phylo'),
]
