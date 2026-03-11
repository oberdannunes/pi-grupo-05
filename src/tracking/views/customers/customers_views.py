from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render (request, "customers/customers_list.html")
