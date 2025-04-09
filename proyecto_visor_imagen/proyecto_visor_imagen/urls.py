from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('viewer.urls')),
    path('docs/', include('docspage.urls')),
]

# Servir archivos estaticos en desarrollo y produccion
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Incluso en produccion, intentamos servir archivos estaticos (para Render)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
