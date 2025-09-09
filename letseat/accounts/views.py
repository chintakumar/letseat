from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.utils import timezone
from datetime import timedelta
import random
from .models import User, PhoneOTP

from .forms import RegistrationForm, EmailLoginForm, PhoneRequestForm, OTPForm
from .utils import send_otp_sms

# OTP validity in minutes
OTP_TTL_MINUTES = 5


# ---------------------------
# Register new user
# ---------------------------
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now login.")
            return redirect("accounts:login_choice")
            
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


# ---------------------------
# Email login
# ---------------------------
def login_email(request):
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # authenticate using email as username
            user = authenticate(request, username=email, password=password)
            if user:
                auth_login(request, user)
                return redirect("pages:home")
            else:
                messages.error(request, "Invalid email or password")
    else:
        form = EmailLoginForm()
    return render(request, "accounts/login_email.html", {"form": form})


# ---------------------------
# Request OTP for phone login
# ---------------------------
def login_phone_request(request):
    if request.method == "POST":
        form = PhoneRequestForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]

            # Ensure user exists
            user, created = User.objects.get_or_create(
                phone_number=phone, defaults={"username": phone}
            )

            # Generate 4-digit OTP
            otp = str(random.randint(1000, 9999))

            PhoneOTP.objects.create(phone=phone, otp=otp)

            # Send OTP via SMS or console
            send_otp_sms(phone, otp)

            # Save phone in session
            request.session["otp_phone"] = phone
            messages.info(request, f"OTP sent to {phone}")
            return redirect("accounts:verify_otp")
    else:
        form = PhoneRequestForm()
    return render(request, "accounts/login_phone.html", {"form": form})


# ---------------------------
# Verify OTP
# ---------------------------
def verify_otp(request):
    phone = request.session.get("otp_phone")
    if not phone:
        return redirect("accounts:login_choice")

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_entered = form.cleaned_data["otp"]

            try:
                otp_obj = (
                    PhoneOTP.objects.filter(phone=phone, otp=otp_entered)
                    .latest("created_at")
                )
            except PhoneOTP.DoesNotExist:
                messages.error(request, "Invalid OTP")
                return redirect("accounts:verify_otp")

            # Check OTP expiry
            if otp_obj.created_at < timezone.now() - timedelta(minutes=OTP_TTL_MINUTES):
                messages.error(request, "OTP expired. Please request again.")
                return redirect("accounts:login_phone_request")

            # Authenticate or create user
            user, _ = CustomUser.objects.get_or_create(
                phone_number=phone, defaults={"username": phone}
            )
            auth_login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("home")
    else:
        form = OTPForm()
    return render(request, "accounts/verify_otp.html", {"form": form})


# ---------------------------
# Logout
# ---------------------------
def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


# ---------------------------
# Login choice page (email or phone)
# ---------------------------
def login_choice(request):
    return render(request, "accounts/login_choice.html")
