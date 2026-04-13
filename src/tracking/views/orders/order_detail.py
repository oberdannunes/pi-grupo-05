from django.http import HttpResponse
from django.shortcuts import render

def detail(request):
    cnpj = request.POST.get("cnpj", "")
    nfe = request.POST.get("nfe", "")
    delivered = request.GET.get("delivered", "false").lower() == "true"
    return render(request, "orders/order_detail.html", {"cnpj": cnpj, "nfe": nfe, "delivered": delivered})
