
from django.contrib import admin
from django.urls import path,include
from AuthUser import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", include(urls))
]
