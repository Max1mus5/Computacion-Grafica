from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('viewer.urls')),
    path('docs/', include('docspage.urls')),
]