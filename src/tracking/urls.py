from django.urls import path
from .views.orders import order_detail

app_name = "tracking"

urlpatterns = [
    path("orders/", order_detail.detail, name="order_detail"),
]