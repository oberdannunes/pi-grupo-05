from django.http import HttpResponse
from django.shortcuts import render

def detail(request):
    cnpj = request.POST.get("cnpj", "")
    nfe = request.POST.get("nfe", "")
    delivered = request.GET.get("delivered", "false").lower() == "true"
    
    
    #TODO: implementar a consulta ao banco de dados para obter os detalhes do pedido com base no CNPJ e NFE fornecidos
    template = "orders/order_detail_delivered.html" if delivered else "orders/order_detail_pending.html"
        
    return render(request, template, {"cnpj": cnpj, "nfe": nfe, "delivered": delivered})
