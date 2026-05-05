from django.db import models

class Order(models.Model):
    # Trava de integridade para as regras de logística
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('TRANSITO', 'Em Trânsito'),
        ('ENTREGUE', 'Entregue'),
    ]

    nfe = models.CharField(max_length=20, verbose_name='Número NFE', default='')
    order_date = models.DateField(verbose_name='Data Pedido')
    collection_date = models.DateField(null=True, blank=True, verbose_name='Data Coleta')
    delivery_date = models.DateField(null=True, blank=True, verbose_name='Data Entrega')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Status', default='PENDENTE')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, default=None, verbose_name='Cliente')
    carrier = models.ForeignKey('Carrier', on_delete=models.CASCADE, default=None, verbose_name='Transportadora')

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        # Índices otimizados para o PostgreSQL acelerar as views de consulta
        indexes = [
            models.Index(fields=['nfe']),
            models.Index(fields=['status']),
            models.Index(fields=['order_date']),
        ]
    
    def customer_cnpj(self):
        return self.customer.cnpj
    customer_cnpj.short_description = 'CNPJ Cliente'
    
    def __str__(self):
        return f"NFE: {self.nfe} - {self.get_status_display()}"