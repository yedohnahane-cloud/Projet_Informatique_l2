from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import SignUpForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Votre compte a été créé avec succès.")
            return redirect("signin")
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


def signin_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Connexion réussie.")
            return redirect("home")
        else:
            messages.error(request, "Email ou mot de passe incorrect.")

    return render(request, "accounts/signin.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté.")
    return redirect("signin")

def auth_page_view(request):
    signup_form = SignUpForm()
    return render(request, "accounts/auth.html", {
        "signup_form": signup_form
    })