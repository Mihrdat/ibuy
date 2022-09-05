from django.contrib import admin
from django.urls import path, include

LOCAL_URLS = [
    path('admin/', admin.site.urls),
]

THIRD_PARTY_URLS = [
    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns = LOCAL_URLS + THIRD_PARTY_URLS
