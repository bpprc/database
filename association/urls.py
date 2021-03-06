from django.urls import path

from association import views

urlpatterns = [
    path(
        "data_association_links/",
        views.data_association_links,
        name="data_association_links",
    ),
    path(
        "example_content/",
        views.example_content,
        name="example_content",
    ),
    path("data_teams/", views.data_teams, name="data_teams"),
    path("list_proteins/", views.list_proteins, name="list_proteins"),
    path(
        "search_association/",
        views.search_association,
        name="search_association",
    ),
    path(
        "search_data_association/",
        views.search_data_association,
        name="search_data_association",
    ),
    path(
        "display_protein_data/<slug:name>/",
        views.display_protein_data,
        name="display_protein_data",
    ),
    path(
        "keyword_confirm/<slug:name>/",
        views.keyword_confirm,
        name="keyword_confirm",
    ),
    path("api", views.home, name="home"),
    path(
        "heatmap_activity",
        views.heatmap_activity,
        name="heatmap_activity",
    ),
    path(
        "metadatabase_protein_detail/<slug:name>/",
        views.metadatabase_protein_detail,
        name="metadatabase_protein_detail",
    ),
]
