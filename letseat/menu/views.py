from django.shortcuts import render
from .models import FoodItem, FoodCategory

def menu_list(request):
    category = request.GET.get("category")   # starters, chinese, etc.
    food_type = request.GET.get("type")      # veg / non-veg

    items = FoodItem.objects.all()

    if category:
        items = items.filter(category__name__iexact=category)
    if food_type:
        items = items.filter(is_veg=(food_type.lower() == "veg"))

    categories = FoodCategory.objects.all()

    return render(request, "menu/menu_list.html", {
        "items": items,
        "categories": categories,
        "selected_category": category,
        "selected_type": food_type,
    })
