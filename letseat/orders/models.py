from django.db import models
from django.contrib.auth.models import User
from menu.models import FoodItem
from django.conf import settings
from django.db import models
from menu.models import MenuItem 
class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 👈 instead of "auth.User"
        on_delete=models.CASCADE,
        related_name="orders"
    )
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_served = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.food_item.name} x {self.quantity}"
