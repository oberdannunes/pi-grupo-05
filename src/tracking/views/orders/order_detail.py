from django.http import HttpResponse
from django.shortcuts import render

def detail(request, order_id):
    return render(request, "orders/order_detail.html", {"order_id": order_id})
