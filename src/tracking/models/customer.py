from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, default='')
    cnpj = models.CharField(max_length=14, verbose_name='CNPJ', default='')
    city = models.ForeignKey('City', on_delete=models.CASCADE)

    class Meta:
        # Índices otimizados para o PostgreSQL acelerar as views de consulta
        indexes = [
            models.Index(fields=['cnpj'])
        ]

    def __str__(self):
        return self.name