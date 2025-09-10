from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/email/", views.login_email, name="login_email"),
    path("logout/", views.logout_view, name="logout"),

]
