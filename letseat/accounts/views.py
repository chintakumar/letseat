from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from .forms import RegistrationForm, EmailLoginForm

# ---------------------------
# Register new user
# ---------------------------
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now login.")
            return redirect("accounts:login_email")  # directly to email login
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
# Logout
# ---------------------------
def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("pages:home")
