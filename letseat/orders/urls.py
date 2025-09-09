from django.urls import path
from . import views

urlpatterns = [
    path("create/<int:item_id>/", views.order_create, name="order_create"),
    path("<int:order_id>/", views.order_detail, name="order_detail"),
]
