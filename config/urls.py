from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('apps.core.urls')),
    path('vuelos/', include('apps.vuelos.urls')),
    path('hoteles/', include('apps.hoteles.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('affiliates/', include('apps.affiliates.urls')),
]

# Debug Toolbar solo en desarrollo
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
