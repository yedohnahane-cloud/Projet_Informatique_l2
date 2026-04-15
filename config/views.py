from django.shortcuts import render

def home_view(request):
    return render(request, "home/acceuil.html")

def about_us_view(request):
    return render(request, "home/aboutUs.html")