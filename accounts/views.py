from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import SignUpForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("subjects_page")

    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre compte a été créé avec succès.")
            return redirect("signin")

    return render(request, "accounts/signup.html", {"form": form})


def signin_view(request):
    if request.user.is_authenticated:
        return redirect("subjects_page")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Connexion réussie.")
            return redirect("subjects_page")

        messages.error(request, "Email ou mot de passe incorrect.")

    return render(request, "accounts/signin.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté.")
    return redirect("signin")

def leo_choisi_view(request):
    return render(request, "accounts/leo_choisi.html")

def lucie_choisi_view(request):
    return render(request, "accounts/lucie_choisi.html")

from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":

        # Modifier username
        if "update_username" in request.POST:
            username = request.POST.get("username")
            user.username = username
            user.save()
            messages.success(request, "Nom d'utilisateur mis à jour.")

        # Modifier email
        if "update_email" in request.POST:
            email = request.POST.get("email")
            user.email = email
            user.save()
            messages.success(request, "Email mis à jour.")

        return redirect("profile")

    return render(request, "accounts/profil-utilisateur.html")