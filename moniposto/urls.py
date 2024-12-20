from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pagina.urls')),  # Incluindo as URLs do app 'pagina'
    path('accounts/', include('django.contrib.auth.urls')),
]
