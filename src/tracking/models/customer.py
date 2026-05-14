from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, default='')
    cnpj = models.CharField(max_length=14, verbose_name='CNPJ', unique=True)
    city = models.ForeignKey('City', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        # Índices otimizados para o PostgreSQL acelerar as views de consulta
        indexes = [
            models.Index(fields=['cnpj'])
        ]

    def __str__(self):
        return self.name