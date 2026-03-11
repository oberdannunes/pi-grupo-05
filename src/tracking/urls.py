from django.urls import path
from .views.carriers import carriers_views
from .views.orders import orders_views
from .views.customers import customers_views

app_name = "tracking"

urlpatterns = [
    path("orders/", orders_views.index, name="orders"),
    path("customers/", customers_views.index, name="customers"),
    path("carriers/", carriers_views.index, name="carriers"),

]