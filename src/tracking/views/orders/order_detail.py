from django.shortcuts import render
from tracking.models.order import Order
from tracking.models.customer import Customer

def detail(request):
    cnpj = request.POST.get("cnpj", "")
    nfe = request.POST.get("nfe", "")
    error = ""

    if request.method == "POST" and cnpj and nfe:
        # tira pontos, barras e tracos do cnpj pra comparar so os numeros
        cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "")

        try:
            cliente = Customer.objects.get(cnpj=cnpj_limpo)
            pedido = Order.objects.get(nfe=nfe, customer=cliente)

            if pedido.delivery_date:
                return render(request, "orders/order_detail_delivered.html", {
                    "pedido": pedido,
                })
            else:
                return render(request, "orders/order_detail_pending.html", {
                    "pedido": pedido,
                })

        except (Customer.DoesNotExist, Order.DoesNotExist):
            error = "Nenhum pedido encontrado para os dados informados."

    return render(request, "core/home_index.html", {"error": error})