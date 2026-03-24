from django.urls import path
from .views.orders import order_detail

app_name = "tracking"

urlpatterns = [
    path("orders/<int:order_id>/", order_detail.detail, name="order_detail"),
]