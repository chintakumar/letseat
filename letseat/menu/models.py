from django.db import models

class FoodCategory(models.Model):
    name = models.CharField(max_length=100)  # Starters, Chinese, Desserts, Drinks, etc.
    is_veg = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Food Categories"

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_veg = models.BooleanField(default=True)
    image = models.ImageField(upload_to="menu/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({'Veg' if self.is_veg else 'Non-Veg'})"
from django.db import models


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ("starter", "Starter"),
        ("chinese", "Chinese"),
        ("main", "Main Course"),
        ("dessert", "Dessert"),
        ("drink", "Drink"),
    ]

    VEG_CHOICES = [
        ("veg", "Vegetarian"),
        ("non-veg", "Non-Vegetarian"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    veg_type = models.CharField(max_length=10, choices=VEG_CHOICES)
    image = models.ImageField(upload_to="menu_images/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_veg_type_display()})"
