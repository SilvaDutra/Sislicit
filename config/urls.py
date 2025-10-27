# Arquivo: config/urls.py

from django.contrib import admin
from django.urls import path, include # Adicione 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    # Inclui todas as URLs do nosso app 'core'
    path('', include('core.urls')),
]