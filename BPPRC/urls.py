from django.contrib import admin
from django.conf.urls.static import static, settings
from django.urls import path, include

handler404 = 'database.views.page_not_found'
handler500 = 'database.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('database.urls')),
    path('', include('bestmatchfinder.urls')),
    path('', include('namingalgorithm.urls')),
    path('', include('clustalanalysis.urls')),
    path('', include('extra.urls')),
    path('', include('graphs.urls')),
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
