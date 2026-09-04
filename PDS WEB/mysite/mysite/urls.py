from django.contrib import admin
from django.urls import path, include
from ficha.views import register

urlpatterns = [
    path("index/", include("index.urls")),
    path("", include("ficha.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", register, name="register"),
]
