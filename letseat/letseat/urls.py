from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("orders/", include("orders.urls")),
    path("menu/", include("menu.urls", namespace="menu")),
    path("", include("pages.urls")),  # home page
]