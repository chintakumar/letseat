from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from menu.models import FoodItem
from .models import Order, OrderItem

from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def order_create(request, item_id):
    # If somehow this is called by a non-logged-in user
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to place an order.")
        return redirect('accounts:login_email')

    item = get_object_or_404(FoodItem, id=item_id)

    # Get quantity from query parameters (default to 1 if not provided)
    quantity = int(request.GET.get('quantity', 1))
    if quantity < 1:
        quantity = 1

    # Check if there's an existing open order for this user
    order, created = Order.objects.get_or_create(user=request.user, is_served=False)

    # Add item to order or update quantity if exists
    order_item, created_item = OrderItem.objects.get_or_create(order=order, food_item=item)
    if not created_item:
        order_item.quantity += quantity
    else:
        order_item.quantity = quantity
    order_item.save()

    return redirect("orders:order_detail", order_id=order.id)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.orderitem_set.all()

    # Prepare a list of dicts with item info and total
    items_with_total = [
        {
            "item": item,
            "total_price": item.quantity * item.food_item.price
        }
        for item in order_items
    ]

    # Total order amount
    total_amount = sum(d["total_price"] for d in items_with_total)

    return render(request, "orders/order_detail.html", {
        "order": order,
        "items_with_total": items_with_total,
        "total_amount": total_amount,
    })

