from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/email/", views.login_email, name="login_email"),
    path("login/phone/", views.login_phone_request, name="login_phone"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("logout/", views.logout_view, name="logout"),
    path("login/", views.login_choice, name="login_choice"),

]
