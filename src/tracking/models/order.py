from django.db import models

class Order(models.Model):
    nfe = models.CharField(max_length=20, verbose_name='Número NFE', default='')
    order_date = models.DateField(verbose_name='Data Pedido')
    delivery_date = models.DateField(null=True, blank=True, verbose_name='Data Entrega')
    status = models.CharField(max_length=20, verbose_name='Status', default='')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, default=None, verbose_name='Cliente')
    carrier = models.ForeignKey('Carrier', on_delete=models.CASCADE, default=None, verbose_name='Transportadora')

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
    
    def __str__(self):
        return str(self.order_date)