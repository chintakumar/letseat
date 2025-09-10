from django.shortcuts import render
from menu.models import FoodItem

def home(request):
    items = FoodItem.objects.all()
    return render(request, "pages/home.html", {"items": items})


def contact(request):
    return render(request, "pages/contact.html")

