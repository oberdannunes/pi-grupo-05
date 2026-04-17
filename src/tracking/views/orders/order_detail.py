from django.http import HttpResponse
from django.shortcuts import render

def detail(request):
    cnpj = request.POST.get("cnpj", "")
    nfe = request.POST.get("nfe", "")
    delivered = request.GET.get("delivered", "false").lower() == "true"
    
    
    #implementar a consulta ao banco de dados para obter os detalhes do pedido com base no CNPJ e NFE fornecidos
    
        
    return render(request, "orders/order_detail.html", {"cnpj": cnpj, "nfe": nfe, "delivered": delivered})
