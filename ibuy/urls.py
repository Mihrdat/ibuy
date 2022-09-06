from django.contrib import admin
from django.urls import path, include

LOCAL_URLS = [
    path('admin/', admin.site.urls),
    path('store/', include('store.urls')),
]

THIRD_PARTY_URLS = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns = LOCAL_URLS + THIRD_PARTY_URLS
