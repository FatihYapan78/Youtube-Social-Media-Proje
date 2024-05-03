from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from Appsocialmedia.views import *
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("profil/<slug:username>", profil, name="profil"),
    path("search/", Search, name="search"),
    path("login/", Login, name="login"),
    path("register/", Register, name="register"),
    path("logout/", Logout, name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
