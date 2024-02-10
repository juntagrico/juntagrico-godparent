"""
test URL Configuration for juntagrico_godparent development
"""
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('impersonate/', include('impersonate.urls')),
    path('', include('juntagrico_godparent.urls')),
    path('', include('juntagrico.urls')),
]
