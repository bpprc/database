from django.contrib import admin
from django.conf.urls.static import static, settings
from django.urls import path, include
from django.contrib.auth import views as auth_views

handler404 = 'database.views.page_not_found'
handler500 = 'database.views.server_error'

urlpatterns = [
    path('prc2020_admin/', admin.site.urls),
    path(
        'admin/password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='admin_password_reset',
    ),
    path(
        'admin/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'admin/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'admin/reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('database.urls')),
    path('', include('bestmatchfinder.urls')),
    path('', include('namingalgorithm.urls')),
    path('', include('clustalanalysis.urls')),
    path('', include('extra.urls')),
    path('', include('graphs.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
