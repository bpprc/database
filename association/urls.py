from django.urls import path
from association import views

urlpatterns = [
    path('data_association_links/', views.data_association_links,
         name='data_association_links'),
    path('example_content/', views.example_content,
         name='example_content'),
    path('data_teams/', views.data_teams,
         name='data_teams'),
    path('list_proteins/', views.list_proteins,
         name='list_proteins'),
]
