from django.contrib import admin
from django.urls import path, include
from graphs import views

urlpatterns = [
    path('graphs_home/', views.graphs_home ,name='graphs_home'),
    path('combo/', views.combo ,name='combo'),
    path("programming/", views.programming, name="programming"),
    path("multiplot/", views.multiplot, name="multiplot"),
    path("products/", views.products, name="products"),
    path("pie/", views.pie, name="pie"),
    path("test_html/", views.test_html, name="test_html"),
    path("protein_table/", views.protein_table, name="protein_table"),
]
