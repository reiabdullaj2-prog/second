from django.urls import path, include
from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('leket.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]