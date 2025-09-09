from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from menu.models import FoodItem
from .models import Order, OrderItem

@login_required
def order_create(request, item_id):
    item = get_object_or_404(FoodItem, id=item_id)

    order = Order.objects.create(user=request.user)
    OrderItem.objects.create(order=order, food_item=item, quantity=1)

    return redirect("order_detail", order.id)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})
