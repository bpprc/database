from django.conf.urls.static import settings, static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

handler404 = "extra.views.page_not_found"
handler500 = "extra.views.server_error"

admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "admin/password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="admin_password_reset",
    ),
    path(
        "admin/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "admin/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "admin/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("accounts/", include("allauth.urls")),
    path("", include("database.urls")),
    path("", include("bestmatchfinder.urls")),
    path("", include("namingalgorithm.urls")),
    path("", include("clustalanalysis.urls")),
    path("", include("extra.urls")),
    path("", include("graphs.urls")),
    path("", include("association.urls")),
    path("", include("api.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# https://stackoverflow.com/questions/20997863/add-a-prefix-to-url-patterns-in-django
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('database/', include('database.urls')),
#     path('database/', include('bestmatchfinder.urls')),
#     path('database/', include('namingalgorithm.urls')),
#     path('database/', include('clustalanalysis.urls')),
#     path('database/', include('extra.urls')),
#     path('database/', include('graphs.urls')),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
