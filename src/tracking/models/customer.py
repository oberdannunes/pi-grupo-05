from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, default='')
    cnpj = models.CharField(max_length=14, verbose_name='CNPJ', default='')
    city = models.ForeignKey('City', on_delete=models.CASCADE)

    def __str__(self):
        return self.name