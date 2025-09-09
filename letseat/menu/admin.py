# menu/admin.py
from django.contrib import admin
from .models import FoodItem, FoodCategory

@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_veg', 'price')
    list_filter = ('category', 'is_veg')
    search_fields = ('name',)
