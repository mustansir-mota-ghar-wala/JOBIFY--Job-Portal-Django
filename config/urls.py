from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('jobs/', include('apps.jobs.urls')),
    path('applications/', include('apps.applications.urls')),
    path('api/', include('apps.accounts.api.urls')),
    path('api/', include('apps.jobs.api.urls')),
    path('api/', include('apps.applications.api.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
